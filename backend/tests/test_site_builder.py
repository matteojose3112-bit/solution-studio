from io import BytesIO
from zipfile import ZipFile

import pytest

from app.services.site_builder import generate_site_package


def sample_payload():
    return {
        "business_name": "Northstar Studio",
        "tagline": "Make your next move count.",
        "description": "Practical services for growing businesses.",
        "services": ["Operations support", "CRM setup"],
        "contact_email": "hello@example.com",
        "accent_color": "#7CE0B5",
    }


def test_generates_static_website_archive():
    filename, archive = generate_site_package(sample_payload())
    assert filename == "northstar-studio-website.zip"
    with ZipFile(BytesIO(archive)) as bundle:
        assert set(bundle.namelist()) == {"index.html", "styles.css", "README.md"}
        html = bundle.read("index.html").decode()
        assert "Northstar Studio" in html
        assert "mailto:hello@example.com" in html
        assert "Operations support" in html


def test_escapes_user_supplied_html():
    payload = sample_payload()
    payload["business_name"] = '<script>alert("x")</script>'
    _, archive = generate_site_package(payload)
    with ZipFile(BytesIO(archive)) as bundle:
        html = bundle.read("index.html").decode()
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


@pytest.mark.parametrize("field,value", [
    ("accent_color", "red"),
    ("contact_email", "not-an-email"),
    ("services", []),
])
def test_rejects_invalid_site_configuration(field, value):
    payload = sample_payload()
    payload[field] = value
    with pytest.raises(ValueError):
        generate_site_package(payload)
