from fastapi.testclient import TestClient

from app.main import app
from app.services.csv_tools import CSVProcessingError, clean_table, inspect_table, parse_csv

client = TestClient(app)


def test_inspect_csv_counts_and_preview() -> None:
    table = parse_csv(b"name,city\\nAda,London\\n,\\nLinus,Helsinki\\n")
    result = inspect_table(table)
    assert result["row_count"] == 3
    assert result["column_count"] == 2
    assert result["empty_rows"] == 1
    assert result["preview"][0] == ["Ada", "London"]


def test_duplicate_headers_are_made_unique() -> None:
    table = parse_csv(b"email,email,\\nfirst,second,third\\n")
    assert table.headers == ["email", "email_2", "column_3"]


def test_cleanup_trims_and_removes_empty_and_duplicate_rows() -> None:
    table = parse_csv(b"name,city\\n Ada , Rome \\n\\nAda,Rome\\nBea,Paris\\n")
    cleaned, stats = clean_table(table)
    assert cleaned.rows == [["Ada", "Rome"], ["Bea", "Paris"]]
    assert stats["removed_empty_rows"] == 1
    assert stats["removed_duplicate_rows"] == 1
    assert stats["trimmed_cells"] == 2


def test_rejects_non_utf8_input() -> None:
    try:
        parse_csv(b"name\\n\\xff")
        assert False, "Expected invalid encoding to be rejected"
    except CSVProcessingError as exc:
        assert "UTF-8" in str(exc)


def test_inspect_endpoint_accepts_csv_upload() -> None:
    response = client.post(
        "/api/data/inspect",
        files={"file": ("sample.csv", b"item,qty\\nPen,2\\nBook,3\\n", "text/csv")},
    )
    assert response.status_code == 200
    assert response.json()["row_count"] == 2
    assert response.json()["columns"][0]["name"] == "item"


def test_inspect_endpoint_rejects_other_extensions() -> None:
    response = client.post(
        "/api/data/inspect",
        files={"file": ("sample.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


def test_clean_endpoint_returns_csv_attachment() -> None:
    response = client.post(
        "/api/data/clean",
        files={"file": ("sample.csv", b"name,city\\n Ada , Rome \\nAda,Rome\\nBea,Paris\\n", "text/csv")},
    )
    assert response.status_code == 200
    assert "attachment" in response.headers["content-disposition"]
    assert response.text == "name,city\\nAda,Rome\\nBea,Paris\\n"
    assert response.headers["x-rows-removed-duplicates"] == "1"
