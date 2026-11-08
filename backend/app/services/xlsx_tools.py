"""Safe XLSX inspection and export helpers. Only the first worksheet is processed."""
from datetime import date, datetime, time
from io import BytesIO
from openpyxl import Workbook, load_workbook
from openpyxl.cell import WriteOnlyCell
from app.services.csv_tools import CSVProcessingError, CSVTable, MAX_COLUMNS, MAX_FILE_BYTES, MAX_ROWS


def parse_xlsx(content: bytes) -> CSVTable:
    if not content:
        raise CSVProcessingError("The uploaded file is empty.")
    if len(content) > MAX_FILE_BYTES:
        raise CSVProcessingError("File exceeds the 5 MB upload limit.")
    try:
        workbook = load_workbook(BytesIO(content), read_only=True, data_only=True)
    except Exception as exc:
        raise CSVProcessingError("Could not read this XLSX file. Please upload a valid .xlsx workbook.") from exc
    try:
        if not workbook.worksheets:
            raise CSVProcessingError("The workbook does not contain a worksheet.")
        iterator = workbook.worksheets[0].iter_rows(values_only=True)
        raw_header = next(iterator, None)
        if raw_header is None:
            raise CSVProcessingError("The worksheet does not contain a header row.")
        headers = [str(v).strip() if v is not None else "" for v in raw_header]
        while headers and not headers[-1]:
            headers.pop()
        if not headers or all(not h for h in headers):
            raise CSVProcessingError("The worksheet header row is blank.")
        if len(headers) > MAX_COLUMNS:
            raise CSVProcessingError(f"XLSX exceeds the {MAX_COLUMNS}-column limit.")
        seen, normalized = {}, []
        for index, header in enumerate(headers, 1):
            base = header or f"column_{index}"
            seen[base] = seen.get(base, 0) + 1
            normalized.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
        rows = []
        for row_number, raw in enumerate(iterator, 2):
            values = list(raw[:len(headers)]) + [None] * max(0, len(headers) - len(raw))
            if any(v is not None for v in values):
                rows.append([_cell_text(v) for v in values])
            if row_number - 1 > MAX_ROWS:
                raise CSVProcessingError(f"XLSX exceeds the {MAX_ROWS:,}-row limit.")
        return CSVTable(normalized, rows, ",")
    finally:
        workbook.close()


def _cell_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    return str(value)


def serialize_xlsx(table: CSVTable) -> bytes:
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("Cleaned data")
    for row in [table.headers, *table.rows]:
        cells = []
        for value in row:
            text = str(value)
            cell = WriteOnlyCell(sheet, value=text)
            if text.startswith(("=", "+", "-", "@")):
                cell.data_type = "s"
            cells.append(cell)
        sheet.append(cells)
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
