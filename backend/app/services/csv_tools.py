"""Safe, dependency-light CSV inspection and cleanup utilities."""

import csv
import io
import re
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from collections import Counter
from dataclasses import dataclass

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_ROWS = 20_000
MAX_COLUMNS = 100
ALLOWED_DELIMITERS = (",", ";", "\t", "|")


class CSVProcessingError(ValueError):
    """Raised when an uploaded CSV cannot be processed safely."""


@dataclass
class CSVTable:
    headers: list[str]
    rows: list[list[str]]
    delimiter: str


def parse_csv(content: bytes) -> CSVTable:
    if not content:
        raise CSVProcessingError("The uploaded file is empty.")
    if len(content) > MAX_FILE_BYTES:
        raise CSVProcessingError("File exceeds the 5 MB upload limit.")
    if b"\x00" in content:
        raise CSVProcessingError("The file contains invalid null bytes.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CSVProcessingError("Please upload a UTF-8 encoded CSV file.") from exc

    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters="".join(ALLOWED_DELIMITERS))
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ","

    try:
        reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True)
        raw_rows = list(reader)
    except csv.Error as exc:
        raise CSVProcessingError(f"Could not parse CSV: {exc}") from exc

    if not raw_rows:
        raise CSVProcessingError("The CSV does not contain a header row.")
    headers = [cell.strip() for cell in raw_rows[0]]
    if not headers or all(not header for header in headers):
        raise CSVProcessingError("The CSV header row is blank.")
    if len(headers) > MAX_COLUMNS:
        raise CSVProcessingError(f"CSV exceeds the {MAX_COLUMNS}-column limit.")

    seen: Counter[str] = Counter()
    normalized_headers: list[str] = []
    for index, header in enumerate(headers, start=1):
        base = header or f"column_{index}"
        seen[base] += 1
        normalized_headers.append(base if seen[base] == 1 else f"{base}_{seen[base]}")

    rows: list[list[str]] = []
    for line_number, row in enumerate(raw_rows[1:], start=2):
        if len(row) > len(normalized_headers):
            raise CSVProcessingError(
                f"Row {line_number} has more cells than the header ({len(row)} vs {len(normalized_headers)})."
            )
        rows.append(row + [""] * (len(normalized_headers) - len(row)))
        if len(rows) > MAX_ROWS:
            raise CSVProcessingError(f"CSV exceeds the {MAX_ROWS:,}-row limit.")

    return CSVTable(normalized_headers, rows, delimiter)


def _value_type(value: str) -> str:
    text = value.strip()
    lowered = text.casefold()
    if lowered in {"true", "false", "yes", "no", "y", "n"}:
        return "boolean"
    if re.fullmatch(r"[+-]?0\d+", text):
        return "text"
    if re.fullmatch(r"[+-]?\d+", text):
        return "integer"
    try:
        number = Decimal(text.replace(",", "")) if "," in text and "." not in text else Decimal(text)
        if number.is_finite():
            return "decimal" if number != number.to_integral_value() or "." in text else "integer"
    except InvalidOperation:
        pass
    try:
        date.fromisoformat(text)
        return "date"
    except ValueError:
        pass
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
        return "datetime"
    except ValueError:
        return "text"


def inspect_table(table: CSVTable) -> dict:
    nonempty_rows = [row for row in table.rows if any(cell.strip() for cell in row)]
    columns = []
    for index, name in enumerate(table.headers):
        values = [row[index] for row in table.rows]
        populated = [value for value in values if value.strip()]
        type_counts = Counter(_value_type(value) for value in populated)
        inferred_type = "empty"
        inconsistent = 0
        if type_counts:
            ranked = type_counts.most_common()
            if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
                inferred_type = "mixed"
                inconsistent = len(populated)
            else:
                inferred_type = ranked[0][0]
                inconsistent = len(populated) - ranked[0][1]
        columns.append({
            "name": name,
            "non_empty": len(populated),
            "empty": len(values) - len(populated),
            "unique": len(set(populated)),
            "inferred_type": inferred_type,
            "inconsistent_values": inconsistent,
            "missing_values": len(values) - len(populated),
        })
    return {
        "row_count": len(table.rows),
        "column_count": len(table.headers),
        "empty_rows": len(table.rows) - len(nonempty_rows),
        "duplicate_rows": len(table.rows) - len({tuple(row) for row in table.rows}),
        "delimiter": "TAB" if table.delimiter == "\t" else table.delimiter,
        "columns": columns,
        "preview": table.rows[:10],
    }


def clean_table(
    table: CSVTable,
    *,
    trim_whitespace: bool = True,
    remove_empty_rows: bool = True,
    remove_duplicate_rows: bool = True,
) -> tuple[CSVTable, dict[str, int]]:
    cleaned: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    removed_empty = 0
    removed_duplicates = 0
    trimmed_cells = 0

    for row in table.rows:
        values = [cell.strip() for cell in row] if trim_whitespace else list(row)
        trimmed_cells += sum(before != after for before, after in zip(row, values))
        if remove_empty_rows and not any(cell.strip() for cell in values):
            removed_empty += 1
            continue
        key = tuple(values)
        if remove_duplicate_rows and key in seen:
            removed_duplicates += 1
            continue
        seen.add(key)
        cleaned.append(values)

    return CSVTable(table.headers, cleaned, table.delimiter), {
        "trimmed_cells": trimmed_cells,
        "removed_empty_rows": removed_empty,
        "removed_duplicate_rows": removed_duplicates,
    }


def serialize_csv(table: CSVTable) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=table.delimiter, lineterminator="\n")
    writer.writerow(table.headers)
    writer.writerows(table.rows)
    return output.getvalue()


def transform_table(table: CSVTable, *, rename_columns: dict[str, str] | None = None, normalize_headers: bool = False, keep_columns: list[str] | None = None) -> CSVTable:
    """Apply explicit, validated column transformations without changing cell values."""
    rename_columns = rename_columns or {}
    if not isinstance(rename_columns, dict):
        raise CSVProcessingError("Column renames must be a JSON object.")
    unknown = set(rename_columns) - set(table.headers)
    if unknown:
        raise CSVProcessingError(f"Unknown columns in rename mapping: {', '.join(sorted(unknown))}.")
    if any(not isinstance(value, str) or not value.strip() for value in rename_columns.values()):
        raise CSVProcessingError("New column names must be non-empty strings.")
    headers = [rename_columns.get(name, name).strip() for name in table.headers]
    if normalize_headers:
        normalized, used = [], Counter()
        for index, name in enumerate(headers, 1):
            base = re.sub(r"[^a-z0-9]+", "_", name.casefold()).strip("_") or f"column_{index}"
            used[base] += 1
            normalized.append(base if used[base] == 1 else f"{base}_{used[base]}")
        headers = normalized
    if len(set(headers)) != len(headers):
        raise CSVProcessingError("Column names must be unique after renaming.")
    if keep_columns is not None:
        if not isinstance(keep_columns, list) or any(not isinstance(name, str) for name in keep_columns):
            raise CSVProcessingError("Selected columns must be a list of column names.")
        if len(set(keep_columns)) != len(keep_columns):
            raise CSVProcessingError("A column can only be selected once.")
        missing = [name for name in keep_columns if name not in headers]
        if missing:
            raise CSVProcessingError(f"Unknown selected columns: {', '.join(missing)}.")
        indexes = [headers.index(name) for name in keep_columns]
        headers = [headers[i] for i in indexes]
        rows = [[row[i] for i in indexes] for row in table.rows]
    else:
        rows = [list(row) for row in table.rows]
    if not headers:
        raise CSVProcessingError("Select at least one column to export.")
    return CSVTable(headers, rows, table.delimiter)
