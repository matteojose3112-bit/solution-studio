"""Document upload and extraction endpoint."""
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_tools import (
    MAX_DOCUMENT_BYTES,
    DocumentProcessingError,
    extract_document,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/extract")
async def extract_uploaded_document(file: UploadFile = File(...)) -> dict:
    filename = file.filename or ""
    content = await file.read(MAX_DOCUMENT_BYTES + 1)
    if len(content) > MAX_DOCUMENT_BYTES:
        raise HTTPException(status_code=413, detail="Document exceeds the 10 MB upload limit.")
    try:
        return extract_document(filename, content)
    except DocumentProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
