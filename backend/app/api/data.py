"""CSV and XLSX upload, inspection and cleanup endpoints."""
import json
import re
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import Response
from app.services.csv_tools import (
    CSVProcessingError,
    MAX_FILE_BYTES,
    clean_table,
    inspect_table,
    parse_csv,
    serialize_csv,
    transform_table,
)
from app.services.xlsx_tools import parse_xlsx, serialize_xlsx
router = APIRouter(prefix="/data", tags=["data"])
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

async def read_table_upload(file: UploadFile):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".csv", ".xlsx"}:
        raise HTTPException(status_code=400, detail="Please upload a .csv or .xlsx file.")
    content = await file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 5 MB upload limit.")
    try:
        table = parse_csv(content) if suffix == ".csv" else parse_xlsx(content)
    except CSVProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return suffix, table

@router.post("/inspect")
async def inspect_data(file: UploadFile = File(...)) -> dict:
    suffix, table = await read_table_upload(file)
    return {"filename": file.filename, "format": suffix[1:], **inspect_table(table)}

@router.post("/clean")
async def clean_data(file: UploadFile = File(...), trim_whitespace: bool = Query(True),
                     remove_empty_rows: bool = Query(True), remove_duplicate_rows: bool = Query(True)) -> Response:
    suffix, table = await read_table_upload(file)
    cleaned, stats = clean_table(table, trim_whitespace=trim_whitespace,
        remove_empty_rows=remove_empty_rows, remove_duplicate_rows=remove_duplicate_rows)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(file.filename or "data").stem) or "data"
    if suffix == ".xlsx":
        payload, output_name, media_type = serialize_xlsx(cleaned), f"{stem}_cleaned.xlsx", XLSX_MIME
    else:
        payload, output_name, media_type = serialize_csv(cleaned), f"{stem}_cleaned.csv", "text/csv; charset=utf-8"
    return Response(content=payload, media_type=media_type, headers={
        "Content-Disposition": f'attachment; filename="{output_name}"',
        "X-Rows-Remaining": str(len(cleaned.rows)),
        "X-Rows-Removed-Empty": str(stats["removed_empty_rows"]),
        "X-Rows-Removed-Duplicates": str(stats["removed_duplicate_rows"]),
        "X-Cells-Trimmed": str(stats["trimmed_cells"]),
        "Access-Control-Expose-Headers": "X-Rows-Remaining, X-Rows-Removed-Empty, X-Rows-Removed-Duplicates, X-Cells-Trimmed",
    })


@router.post("/transform")
async def transform_data(file: UploadFile = File(...), trim_whitespace: bool = Query(True), remove_empty_rows: bool = Query(True), remove_duplicate_rows: bool = Query(True), normalize_headers: bool = Query(False), rename_columns: str = Query("{}"), keep_columns: str = Query("")) -> Response:
    suffix, table = await read_table_upload(file)
    try:
        rename_mapping = json.loads(rename_columns)
        if not isinstance(rename_mapping, dict):
            raise CSVProcessingError("Column renames must be a JSON object.")
        selected_columns = [name.strip() for name in keep_columns.splitlines() if name.strip()] or None
        transformed = transform_table(table, rename_columns=rename_mapping, normalize_headers=normalize_headers, keep_columns=selected_columns)
        transformed, stats = clean_table(transformed, trim_whitespace=trim_whitespace, remove_empty_rows=remove_empty_rows, remove_duplicate_rows=remove_duplicate_rows)
    except (json.JSONDecodeError, CSVProcessingError) as exc:
        detail = "Column rename mapping must be valid JSON." if isinstance(exc, json.JSONDecodeError) else str(exc)
        raise HTTPException(status_code=422, detail=detail) from exc
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(file.filename or "data").stem) or "data"
    if suffix == ".xlsx": payload, output_name, media_type = serialize_xlsx(transformed), f"{stem}_transformed.xlsx", XLSX_MIME
    else: payload, output_name, media_type = serialize_csv(transformed), f"{stem}_transformed.csv", "text/csv; charset=utf-8"
    return Response(content=payload, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="{output_name}"', "X-Rows-Remaining": str(len(transformed.rows)), "X-Rows-Removed-Empty": str(stats["removed_empty_rows"]), "X-Rows-Removed-Duplicates": str(stats["removed_duplicate_rows"]), "X-Cells-Trimmed": str(stats["trimmed_cells"])})
