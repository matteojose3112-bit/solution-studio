from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_research_report_endpoint_returns_source_references():
    response = client.post("/api/research/report", json={
        "question": "Compare CRM options",
        "sources": [{
            "title": "Vendor overview",
            "url": "https://example.com/crm",
            "notes": "The platform supports contact management and workflow automation."
        }]
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["source_count"] == 1
    assert payload["sources"][0]["url"] == "https://example.com/crm"
    assert payload["key_points"]


def test_research_report_endpoint_rejects_invalid_url():
    response = client.post("/api/research/report", json={
        "question": "Compare options",
        "sources": [{"title": "Unsafe", "url": "javascript:alert(1)", "notes": "Some useful source notes."}]
    })
    assert response.status_code == 422
