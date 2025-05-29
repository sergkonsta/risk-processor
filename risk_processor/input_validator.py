from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict, Optional
import csv

class JsonInputModel(BaseModel):
    city: str
    crime_index: float = Field(..., ge=0, le=10)
    accident_rate: float = Field(..., ge=0, le=10)
    socioeconomic_level: float = Field(..., ge=1, le=10)
    weather_condition: str

class InputValidator:
    @staticmethod
    def validate_json(data: Dict[str, Any]) -> JsonInputModel:
        try:
            return JsonInputModel(**data)
        except ValidationError as e:
            raise ValueError(e.json())

    @staticmethod
    def parse_csv(file_content: str):
        reader = csv.DictReader(file_content.splitlines())
        for idx, row in enumerate(reader):
            try:
                validated = InputValidator.validate_json(row)
                yield idx, validated.dict(), None
            except ValueError as err:
                yield idx, row, str(err)