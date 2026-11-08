from io import BytesIO
from zipfile import ZipFile

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_website_generator_returns_zip_download():
    response = client.post("/api/development/generate", json={
        "business_name": "Example Business",
        "tagline": "A clear promise.",
        "description": "A small business website starter.",
        "services": ["Consulting"],
        "contact_email": "hello@example.com",
        "accent_color": "#336699",
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    with ZipFile(BytesIO(response.content)) as bundle:
        assert "index.html" in bundle.namelist()
