"""Safe, dependency-light CSV inspection and cleanup utilities."""

import csv
import io
from collections import Counter
from dataclasses import dataclass

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_ROWS = 20_000
MAX_COLUMNS = 100
ALLOWED_DELIMITERS = (",", ";", "\\t", "|")


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
    if b"\\x00" in content:
        raise CSVProcessingError("The file contains invalid null bytes.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CSVProcessingError("Please upload a UTF-8 encoded CSV file.") from exc

    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters="".join(ALLOWED_DELIMITERS))
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

    # Give blank and repeated headings stable names so every column is addressable.
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


def inspect_table(table: CSVTable) -> dict:
    nonempty_rows = [row for row in table.rows if any(cell.strip() for cell in row)]
    columns = []
    for index, name in enumerate(table.headers):
        values = [row[index] for row in table.rows]
        populated = [value for value in values if value.strip()]
        columns.append({
            "name": name,
            "non_empty": len(populated),
            "empty": len(values) - len(populated),
            "unique": len(set(populated)),
        })
    return {
        "row_count": len(table.rows),
        "column_count": len(table.headers),
        "empty_rows": len(table.rows) - len(nonempty_rows),
        "duplicate_rows": len(table.rows) - len({tuple(row) for row in table.rows}),
        "delimiter": "TAB" if table.delimiter == "\\t" else table.delimiter,
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
    for row in table.rows:
        values = [cell.strip() for cell in row] if trim_whitespace else list(row)
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
        "trimmed_cells": sum(
            1 for old, new in zip(table.rows, [
                [cell.strip() for cell in row] if trim_whitespace else row for row in table.rows
            ]) for before, after in zip(old, new) if before != after
        ),
        "removed_empty_rows": removed_empty,
        "removed_duplicate_rows": removed_duplicates,
    }


def serialize_csv(table: CSVTable) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, delimiter=table.delimiter, lineterminator="\\n")
    writer.writerow(table.headers)
    writer.writerows(table.rows)
    return output.getvalue()
