import pytest

from app.services.research_tools import ResearchInputError, build_research_report


def test_builds_source_linked_report_from_supplied_notes():
    report = build_research_report("Compare CRM options", [{
        "title": "Vendor overview",
        "url": "https://example.com/crm",
        "notes": "The platform supports contact management. It includes workflow automation for small teams."
    }])
    assert report["source_count"] == 1
    assert report["sources"][0]["id"] == 1
    assert len(report["key_points"]) == 2
    assert "have not been independently verified" in report["executive_summary"]


@pytest.mark.parametrize("url", ["javascript:alert(1)", "file:///etc/passwd", "example.com"])
def test_rejects_non_http_source_urls(url):
    with pytest.raises(ResearchInputError):
        build_research_report("Research question", [{
            "title": "Unsafe source", "url": url, "notes": "A sufficiently long note for testing."
        }])


def test_rejects_duplicate_urls():
    source = {"title": "Source", "url": "https://example.com/page", "notes": "A sufficiently long note for testing."}
    with pytest.raises(ResearchInputError, match="duplicate"):
        build_research_report("Research question", [source, {**source, "title": "Duplicate"}])


def test_requires_source_notes():
    with pytest.raises(ResearchInputError, match="notes"):
        build_research_report("Research question", [{
            "title": "Source", "url": "https://example.com", "notes": ""
        }])
