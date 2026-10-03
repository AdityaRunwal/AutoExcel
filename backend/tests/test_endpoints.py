import sys
import os
import io
import pandas as pd
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app

client = TestClient(app)


def make_csv_bytes(with_duplicates=True, with_missing=True):
    data = {
        "Name": ["Alice", "Bob", "Charlie", "Alice"] if with_duplicates else ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, None, 25] if with_missing and with_duplicates else [25, 30, 35],
    }
    df = pd.DataFrame(data)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return io.BytesIO(buf.getvalue().encode("utf-8"))


def make_empty_csv_bytes():
    df = pd.DataFrame(columns=["Name", "Age"])
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return io.BytesIO(buf.getvalue().encode("utf-8"))


# ---------- /preview-plan ----------

def test_preview_plan_valid_prompt():
    file_bytes = make_csv_bytes()
    response = client.post(
        "/preview-plan",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"prompt": "remove duplicates"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["has_plan"] is True
    assert data["clarification_needed"] is False
    assert len(data["steps"]) >= 1

def test_preview_plan_no_operation_detected():
    file_bytes = make_csv_bytes()
    response = client.post(
        "/preview-plan",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"prompt": "make me a pivot chart"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["has_plan"] is False
    assert data["clarification_needed"] is True
    assert len(data["message"]) > 0

def test_preview_plan_invalid_column_skipped():
    file_bytes = make_csv_bytes()
    response = client.post(
        "/preview-plan",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"prompt": "sort by NotARealColumn descending"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["has_plan"] is False
    assert len(data["skipped_steps"]) == 1

def test_preview_plan_empty_prompt():
    file_bytes = make_csv_bytes()
    response = client.post(
        "/preview-plan",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"prompt": "   "}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["clarification_needed"] is True

def test_preview_plan_empty_file():
    file_bytes = make_empty_csv_bytes()
    response = client.post(
        "/preview-plan",
        files={"file": ("empty.csv", file_bytes, "text/csv")},
        data={"prompt": "remove duplicates"}
    )
    assert response.status_code == 400

def test_preview_plan_unsupported_file_type():
    file_bytes = io.BytesIO(b"not a real dataset")
    response = client.post(
        "/preview-plan",
        files={"file": ("test.txt", file_bytes, "text/plain")},
        data={"prompt": "remove duplicates"}
    )
    assert response.status_code == 400


# ---------- /ai-clean ----------

def test_ai_clean_removes_duplicates():
    file_bytes = make_csv_bytes()
    response = client.post(
        "/ai-clean",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"prompt": "remove duplicates"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] in ("text/csv", "text/csv; charset=utf-8")

def test_ai_clean_no_operation_detected():
    file_bytes = make_csv_bytes()
    response = client.post(
        "/ai-clean",
        files={"file": ("test.csv", file_bytes, "text/csv")},
        data={"prompt": "make me a pivot chart"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "no_operation"

def test_ai_clean_empty_file_rejected():
    file_bytes = make_empty_csv_bytes()
    response = client.post(
        "/ai-clean",
        files={"file": ("empty.csv", file_bytes, "text/csv")},
        data={"prompt": "remove duplicates"}
    )
    assert response.status_code == 400