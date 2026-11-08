"""CSV upload, inspection and cleanup endpoints."""

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import Response

from app.services.csv_tools import (
    CSVProcessingError,
    MAX_FILE_BYTES,
    clean_table,
    inspect_table,
    parse_csv,
    serialize_csv,
)

router = APIRouter(prefix="/data", tags=["data"])


async def read_csv_upload(file: UploadFile) -> bytes:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")
    content = await file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 5 MB upload limit.")
    return content


@router.post("/inspect")
async def inspect_csv(file: UploadFile = File(...)) -> dict:
    content = await read_csv_upload(file)
    try:
        table = parse_csv(content)
    except CSVProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"filename": file.filename, **inspect_table(table)}


@router.post("/clean")
async def clean_csv(
    file: UploadFile = File(...),
    trim_whitespace: bool = Query(True),
    remove_empty_rows: bool = Query(True),
    remove_duplicate_rows: bool = Query(True),
) -> Response:
    content = await read_csv_upload(file)
    try:
        table = parse_csv(content)
        cleaned, stats = clean_table(
            table,
            trim_whitespace=trim_whitespace,
            remove_empty_rows=remove_empty_rows,
            remove_duplicate_rows=remove_duplicate_rows,
        )
    except CSVProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    safe_name = (file.filename or "data").rsplit(".", 1)[0]
    return Response(
        content=serialize_csv(cleaned),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_name}_cleaned.csv"',
            "X-Rows-Remaining": str(len(cleaned.rows)),
            "X-Rows-Removed-Empty": str(stats["removed_empty_rows"]),
            "X-Rows-Removed-Duplicates": str(stats["removed_duplicate_rows"]),
            "X-Cells-Trimmed": str(stats["trimmed_cells"]),
            "Access-Control-Expose-Headers": "X-Rows-Remaining, X-Rows-Removed-Empty, X-Rows-Removed-Duplicates, X-Cells-Trimmed",
        },
    )
