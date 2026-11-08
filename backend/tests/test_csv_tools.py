from fastapi.testclient import TestClient

from app.main import app
from app.services.csv_tools import CSVProcessingError, clean_table, inspect_table, parse_csv, transform_table

client = TestClient(app)


def test_inspect_csv_counts_and_preview() -> None:
    table = parse_csv(b"name,city\nAda,London\n,\nLinus,Helsinki\n")
    result = inspect_table(table)
    assert result["row_count"] == 3
    assert result["column_count"] == 2
    assert result["empty_rows"] == 1
    assert result["preview"][0] == ["Ada", "London"]


def test_duplicate_headers_are_made_unique() -> None:
    table = parse_csv(b"email,email,\nfirst,second,third\n")
    assert table.headers == ["email", "email_2", "column_3"]


def test_cleanup_trims_and_removes_empty_and_duplicate_rows() -> None:
    table = parse_csv(b"name,city\n Ada , Rome \n\nAda,Rome\nBea,Paris\n")
    cleaned, stats = clean_table(table)
    assert cleaned.rows == [["Ada", "Rome"], ["Bea", "Paris"]]
    assert stats["removed_empty_rows"] == 1
    assert stats["removed_duplicate_rows"] == 1
    assert stats["trimmed_cells"] == 2


def test_rejects_non_utf8_input() -> None:
    try:
        parse_csv(b"name\n\xff")
        assert False, "Expected invalid encoding to be rejected"
    except CSVProcessingError as exc:
        assert "UTF-8" in str(exc)


def test_rejects_null_bytes() -> None:
    try:
        parse_csv(b"name\nvalue\x00")
        assert False, "Expected null bytes to be rejected"
    except CSVProcessingError as exc:
        assert "null bytes" in str(exc)


def test_inspect_endpoint_accepts_csv_upload() -> None:
    response = client.post(
        "/api/data/inspect",
        files={"file": ("sample.csv", b"item,qty\nPen,2\nBook,3\n", "text/csv")},
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
        files={"file": ("sample.csv", b"name,city\n Ada , Rome \nAda,Rome\nBea,Paris\n", "text/csv")},
    )
    assert response.status_code == 200
    assert "attachment" in response.headers["content-disposition"]
    assert response.text == "name,city\nAda,Rome\nBea,Paris\n"
    assert response.headers["x-rows-removed-duplicates"] == "1"


def test_column_type_detection_and_validation_warnings() -> None:
    table = parse_csv(
        b"order_id,amount,active,created_at\n0012,12.50,true,2026-01-02\n"
        b"0013,13.75,false,2026-01-03\n0014,not-a-number,yes,invalid-date\n0015,,no,2026-01-04\n"
    )
    columns = inspect_table(table)["columns"]
    assert [column["inferred_type"] for column in columns] == [
        "text", "decimal", "boolean", "date"
    ]
    assert columns[1]["inconsistent_values"] == 1
    assert columns[2]["inconsistent_values"] == 0
    assert columns[3]["inconsistent_values"] == 1
    assert columns[1]["missing_values"] == 1


def test_empty_column_is_reported_without_a_type() -> None:
    table = parse_csv(b"name,notes\nAda,\nBea,\n")
    notes = inspect_table(table)["columns"][1]
    assert notes["inferred_type"] == "empty"
    assert notes["missing_values"] == 2


def test_transform_renames_normalizes_and_reorders_selected_columns() -> None:
    table = parse_csv(b"First Name,Order ID,City\nAda,0012,London\nBea,0013,Paris\n")
    result = transform_table(table, rename_columns={"First Name": "Customer Name"}, normalize_headers=True, keep_columns=["city", "customer_name"])
    assert result.headers == ["city", "customer_name"]
    assert result.rows == [["London", "Ada"], ["Paris", "Bea"]]


def test_transform_rejects_invalid_column_selection() -> None:
    table = parse_csv(b"name,city\nAda,London\n")
    for options in ({"keep_columns": ["missing"]}, {"keep_columns": ["name", "name"]}, {"rename_columns": {"city": "name"}}):
        try:
            transform_table(table, **options)
            assert False, "Expected invalid transformation to be rejected"
        except CSVProcessingError:
            pass


def test_transform_endpoint_exports_selected_columns() -> None:
    response = client.post("/api/data/transform?normalize_headers=true&keep_columns=city%0Aname", files={"file": ("sample.csv", b"Name,City\nAda,London\n", "text/csv")})
    assert response.status_code == 200
    assert response.text == "city,name\nLondon,Ada\n"


def test_transform_endpoint_rejects_invalid_rename_json() -> None:
    response = client.post("/api/data/transform?rename_columns=not-json", files={"file": ("sample.csv", b"name,city\nAda,London\n", "text/csv")})
    assert response.status_code == 422

 

def test_empty_rename_mapping_array_is_rejected() -> None:
    table = parse_csv(b"name,city\nAda,London\n")
    try:
        transform_table(table, rename_columns=[])
        assert False, "Expected a non-object rename mapping to be rejected"
    except CSVProcessingError as exc:
        assert "JSON object" in str(exc)


def test_numeric_inference_does_not_treat_decimal_comma_as_thousands() -> None:
    table = parse_csv(b"amount;other\n1,2;x\n")
    assert inspect_table(table)["columns"][0]["inferred_type"] == "text"



def test_csv_export_neutralizes_spreadsheet_formula_cells() -> None:
    from app.services.csv_tools import CSVTable, serialize_csv

    table = CSVTable(
        headers=["=HYPERLINK(\"https://example.com\")", "amount"],
        rows=[["@SUM(1,1)", "-2",]],
        delimiter=",",
    )
    exported = serialize_csv(table)
    assert "\"'=HYPERLINK" in exported
    assert "'@SUM(1,1)" in exported
    assert "'-2" in exported
