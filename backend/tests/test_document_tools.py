from io import BytesIO

import pytest
from docx import Document

from app.services.document_tools import DocumentProcessingError, extract_document


def make_docx() -> bytes:
    document = Document()
    document.core_properties.title = "Quarterly overview"
    document.add_paragraph("Revenue increased during the quarter.")
    table = document.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Region"
    table.rows[0].cells[1].text = "North"
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def test_extracts_text_and_metadata_from_docx():
    result = extract_document("overview.docx", make_docx())
    assert result["format"] == "docx"
    assert result["metadata"]["title"] == "Quarterly overview"
    assert "Revenue increased" in result["text"]
    assert "Region | North" in result["text"]


def test_extracts_utf8_text_file():
    result = extract_document("notes.txt", b"First line\nSecond line")
    assert result["word_count"] == 4
    assert result["text"] == "First line\nSecond line"


@pytest.mark.parametrize("filename,content", [
    ("unknown.exe", b"not a document"),
    ("notes.txt", b"\xff\xfe"),
    ("broken.docx", b"not a zip archive"),
    ("broken.pdf", b"not a pdf"),
])
def test_rejects_unsupported_or_invalid_documents(filename, content):
    with pytest.raises(DocumentProcessingError):
        extract_document(filename, content)


def test_rejects_empty_documents():
    with pytest.raises(DocumentProcessingError, match="empty"):
        extract_document("empty.txt", b"")
