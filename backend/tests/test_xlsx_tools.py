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
