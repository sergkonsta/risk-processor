import json
import pytest
from pathlib import Path
from risk_processor.input_validator import InputValidator, JsonInputModel


def test_validate_json_success():
    mock_file = Path(__file__).parent / 'mock' / 'mock_input.json'
    data = json.loads(mock_file.read_text())
    model = InputValidator.validate_json(data)
    assert isinstance(model, JsonInputModel)
    assert model.dict() == data


def test_validate_json_failure_missing_field():
    invalid = {"crime_index": 5.5}
    with pytest.raises(ValueError):
        InputValidator.validate_json(invalid)