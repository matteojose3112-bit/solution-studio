from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_extract_document_endpoint():
    response = client.post(
        "/api/documents/extract",
        files={"file": ("notes.txt", b"Client onboarding checklist", "text/plain")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["format"] == "txt"
    assert payload["text"] == "Client onboarding checklist"
    assert payload["word_count"] == 3


def test_extract_document_endpoint_rejects_invalid_format():
    response = client.post(
        "/api/documents/extract",
        files={"file": ("payload.exe", b"content", "application/octet-stream")},
    )
    assert response.status_code == 422
