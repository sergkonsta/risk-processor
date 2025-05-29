from fastapi.testclient import TestClient
import json
from pathlib import Path

from main import app

client = TestClient(app)


def test_process_endpoint_success():
    mock_file = Path(__file__).parent / 'mock' / 'mock_input.json'
    payload = json.loads(mock_file.read_text())
    response = client.post("/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == payload["city"]
    assert "components" in data and "risk_score" in data
    components = data["components"]
    assert set(components.keys()) == {"crime_index", "accident_rate", "socioeconomic_level", "weather_condition"}
    assert isinstance(data["risk_score"], float)


def test_process_endpoint_validation_error():
    payload = {"crime_index": 5.0}
    response = client.post("/process", json=payload)
    assert response.status_code == 422


def test_process_csv_endpoint_success():
    csv_path = Path(__file__).parent / 'mock' / 'mock_input_fully_correct.csv'
    csv_content = csv_path.read_text()
    files = {"file": ("mock_input_fully_correct.csv", csv_content, "text/csv")}
    response = client.post("/process-csv", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment; filename=results.csv" in response.headers.get("Content-Disposition", "")
    text = response.text
    assert "risk_score" in text
    assert "components" in text
    assert "row" in text


def test_process_csv_endpoint_partial_invalid():
    csv_path = Path(__file__).parent / 'mock' / 'mock_input_partially_invalid.csv'
    csv_content = csv_path.read_text()
    files = {"file": ("mock_input_partially_invalid.csv", csv_content, "text/csv")}
    response = client.post("/process-csv", files=files)
    assert response.status_code == 200
    text = response.text
    assert "Chicago" in text
    assert "error" in text
