from io import BytesIO
from openpyxl import Workbook, load_workbook
from fastapi.testclient import TestClient
from app.main import app
from app.services.xlsx_tools import parse_xlsx, serialize_xlsx
from app.services.csv_tools import clean_table, inspect_table
client = TestClient(app)

def sample_xlsx():
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["name", "city"])
    sheet.append([" Ada ", " Rome "])
    sheet.append(["Ada", "Rome"])
    sheet.append([None, None])
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()

def test_xlsx_inspection_and_cleanup():
    table = parse_xlsx(sample_xlsx())
    assert table.headers == ["name", "city"]
    assert inspect_table(table)["row_count"] == 3
    cleaned, stats = clean_table(table)
    assert cleaned.rows == [["Ada", "Rome"]]
    assert stats["removed_duplicate_rows"] == 1
    assert stats["removed_empty_rows"] == 1

def test_xlsx_serialization_writes_values_as_text():
    cleaned, _ = clean_table(parse_xlsx(sample_xlsx()))
    workbook = load_workbook(BytesIO(serialize_xlsx(cleaned)), data_only=False)
    assert workbook.active["A2"].value == "Ada"
    workbook.close()

def test_xlsx_inspect_endpoint():
    response = client.post("/api/data/inspect", files={"file": ("sample.xlsx", sample_xlsx())})
    assert response.status_code == 200
    assert response.json()["format"] == "xlsx"
    assert response.json()["column_count"] == 2

def test_xlsx_clean_endpoint_returns_workbook():
    response = client.post("/api/data/clean", files={"file": ("sample.xlsx", sample_xlsx())})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    workbook = load_workbook(BytesIO(response.content), data_only=True)
    assert workbook.active["A2"].value == "Ada"
    workbook.close()

def test_rejects_invalid_xlsx():
    response = client.post("/api/data/inspect", files={"file": ("broken.xlsx", b"not a workbook")})
    assert response.status_code == 422


def test_xlsx_transform_endpoint_exports_selected_columns() -> None:
    response = client.post(
        "/api/data/transform?normalize_headers=true&keep_columns=city%0Aname",
        files={"file": ("sample.xlsx", sample_xlsx())},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    workbook = load_workbook(BytesIO(response.content), data_only=True)
    assert workbook.active["A1"].value == "city"
    assert workbook.active["B1"].value == "name"
    assert workbook.active["A2"].value == "Rome"
    assert workbook.active["B2"].value == "Ada"
    workbook.close()

 

def test_xlsx_rejects_upload_over_limit() -> None:
    from app.services.csv_tools import CSVProcessingError

    try:
        parse_xlsx(b"x" * (5 * 1024 * 1024 + 1))
        assert False, "Expected oversized workbook to be rejected"
    except CSVProcessingError as exc:
        assert "5 MB" in str(exc)



def test_xlsx_rejects_archive_expansion_over_limit() -> None:
    from zipfile import ZIP_DEFLATED, ZipFile
    from app.services.xlsx_tools import MAX_XLSX_UNCOMPRESSED_BYTES

    archive = BytesIO()
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        bundle.writestr("xl/sharedStrings.xml", b"0" * (MAX_XLSX_UNCOMPRESSED_BYTES + 1))

    try:
        parse_xlsx(archive.getvalue())
        assert False, "Expected oversized archive expansion to be rejected"
    except Exception as exc:
        assert "25 MB" in str(exc)
