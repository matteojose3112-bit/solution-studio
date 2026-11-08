from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_workflow_requires_approval_by_default():
    response = client.post("/api/automation/run", json={
        "input_text": "  Hello   world  ",
        "steps": ["trim_whitespace", "collapse_whitespace"],
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "awaiting_approval"
    assert payload["output"] == "Hello world"


def test_approved_workflow_completes():
    response = client.post("/api/automation/run", json={
        "input_text": "Hello world",
        "steps": ["uppercase"],
        "approval_required": True,
        "approved": True,
    })
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["output"] == "HELLO WORLD"


def test_rejects_too_many_steps():
    response = client.post("/api/automation/run", json={
        "input_text": "Hello",
        "steps": ["trim_whitespace"] * 9,
    })
    assert response.status_code == 422
