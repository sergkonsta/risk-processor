import pytest
from risk_processor.risk_processor import RiskProcessor

def test_process_basic():
    weights = {
        'crime_index': 1.0,
        'accident_rate': 1.0,
        'socioeconomic_level': 1.0,
        'weather_condition': {
            'sunny': 2,
            'rain': 4,
            'snow': 6,
            'armageddon': 9
        }
    }
    noise_level = 2.0
    processor = RiskProcessor(weights=weights, noise_level=noise_level)

    raw = {
        'crime_index': 5.0,
        'accident_rate': 2.0,
        'socioeconomic_level': 8.0,
        'weather_condition': 'armageddon'
    }

    result = processor.process(raw)

    print(result)

    expected_components = {
        'crime_index': 50,
        'accident_rate': 24,
        'socioeconomic_level': 77.77777777777779,
        'weather_condition': 90
    }
    assert result['components'] == pytest.approx(expected_components)