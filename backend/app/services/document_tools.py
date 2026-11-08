"""In-memory extraction for PDF, DOCX and UTF-8 text documents."""
from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from docx import Document
from pypdf import PdfReader

MAX_DOCUMENT_BYTES = 10 * 1024 * 1024
MAX_PDF_PAGES = 100
MAX_DOCX_UNCOMPRESSED_BYTES = 25 * 1024 * 1024
MAX_TEXT_CHARACTERS = 100_000


class DocumentProcessingError(ValueError):
    """Raised when a document cannot be safely extracted."""


def _bounded_text(value: str) -> tuple[str, bool]:
    normalized = value.replace("\x00", "").strip()
    return normalized[:MAX_TEXT_CHARACTERS], len(normalized) > MAX_TEXT_CHARACTERS


def extract_document(filename: str, content: bytes) -> dict:
    suffix = Path(filename or "").suffix.lower()
    if not content:
        raise DocumentProcessingError("The uploaded document is empty.")
    if len(content) > MAX_DOCUMENT_BYTES:
        raise DocumentProcessingError("Document exceeds the 10 MB upload limit.")
    if suffix not in {".pdf", ".docx", ".txt"}:
        raise DocumentProcessingError("Supported formats are PDF, DOCX and TXT.")

    metadata = {}
    if suffix == ".txt":
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise DocumentProcessingError("Please upload a UTF-8 encoded text file.") from exc
        page_count = None
    elif suffix == ".pdf":
        try:
            reader = PdfReader(BytesIO(content), strict=False)
            if reader.is_encrypted and not reader.decrypt(""):
                raise DocumentProcessingError("Password-protected PDFs are not supported.")
            page_count = len(reader.pages)
            if page_count > MAX_PDF_PAGES:
                raise DocumentProcessingError(f"PDF exceeds the {MAX_PDF_PAGES}-page limit.")
            text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
            pdf_metadata = reader.metadata
            if pdf_metadata:
                metadata = {
                    key.lstrip("/").lower(): str(value)
                    for key, value in pdf_metadata.items()
                    if value is not None
                }
        except DocumentProcessingError:
            raise
        except Exception as exc:
            raise DocumentProcessingError("Could not read this PDF. Check that it is a valid, unencrypted PDF.") from exc
    else:
        try:
            with ZipFile(BytesIO(content)) as archive:
                if sum(item.file_size for item in archive.infolist()) > MAX_DOCX_UNCOMPRESSED_BYTES:
                    raise DocumentProcessingError("DOCX expands beyond the 25 MB processing limit.")
            document = Document(BytesIO(content))
            parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
            for table in document.tables:
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells]
                    if any(cells):
                        parts.append(" | ".join(cells))
            text = "\n".join(parts)
            properties = document.core_properties
            metadata = {
                key: value for key, value in {
                    "title": properties.title,
                    "author": properties.author,
                    "subject": properties.subject,
                    "created": properties.created.isoformat() if properties.created else None,
                    "modified": properties.modified.isoformat() if properties.modified else None,
                }.items() if value
            }
            page_count = None
        except DocumentProcessingError:
            raise
        except (BadZipFile, Exception) as exc:
            raise DocumentProcessingError("Could not read this DOCX. Check that it is a valid .docx document.") from exc

    extracted, truncated = _bounded_text(text)
    return {
        "filename": Path(filename).name,
        "format": suffix[1:],
        "metadata": metadata,
        "page_count": page_count,
        "character_count": len(extracted),
        "word_count": len(extracted.split()),
        "truncated": truncated,
        "text": extracted,
    }
