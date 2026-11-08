"""Deterministic research report builder using source notes supplied by the user."""
from collections import OrderedDict
from urllib.parse import urlparse


class ResearchInputError(ValueError):
    """Raised when research input is incomplete or unsafe."""


def build_research_report(question: str, sources: list[dict]) -> dict:
    question = question.strip()
    if not question or len(question) > 500:
        raise ResearchInputError("Enter a research question of 1–500 characters.")
    if not 1 <= len(sources) <= 8:
        raise ResearchInputError("Add between 1 and 8 sources.")

    prepared = []
    seen_urls = set()
    statements = []
    for index, source in enumerate(sources, start=1):
        title = str(source.get("title", "")).strip()
        url = str(source.get("url", "")).strip()
        notes = str(source.get("notes", "")).strip()
        parsed = urlparse(url)
        if not title or len(title) > 200:
            raise ResearchInputError(f"Source {index}: enter a title of 1–200 characters.")
        if not notes or len(notes) > 4000:
            raise ResearchInputError(f"Source {index}: enter notes or an excerpt (1–4,000 characters).")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ResearchInputError(f"Source {index}: use a valid http or https URL.")
        normalized_url = url.rstrip("/")
        if normalized_url in seen_urls:
            raise ResearchInputError(f"Source {index}: duplicate source URL.")
        seen_urls.add(normalized_url)
        prepared.append({"id": index, "title": title, "url": url, "notes": notes})
        for fragment in notes.replace("\n", " ").split(". "):
            text = fragment.strip(" \t\r\n.;")
            if len(text) >= 24 and text.casefold() not in {item.casefold() for item in statements}:
                statements.append(text)

    return {
        "question": question,
        "source_count": len(prepared),
        "sources": [{"id": item["id"], "title": item["title"], "url": item["url"]} for item in prepared],
        "executive_summary": (
            f"This working brief addresses: {question} "
            f"It is based on {len(prepared)} source(s) and the notes supplied for this report. "
            "The findings below are extracted from those notes and have not been independently verified."
        ),
        "key_points": statements[:12],
        "limitations": [
            "This tool organizes user-provided source notes; it does not browse or verify the linked pages.",
            "Check each source directly and confirm dates, context and claims before relying on the report.",
            "The output is a working brief, not professional, legal, medical or financial advice."
        ],
    }
