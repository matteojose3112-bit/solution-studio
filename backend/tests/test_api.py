from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "solution-studio"}


def test_version_endpoint() -> None:
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}


def test_frontend_is_served() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Solution Studio" in response.text
