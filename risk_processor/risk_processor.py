import random
from typing import Dict, Any


class RiskProcessor:
    def __init__(self, weights: Dict, noise_level: float):
        self.weights = weights
        self.noise_level = noise_level

    def _normalize(self, value: float, min_val: float, max_val: float) -> float:
        return (value - min_val) / (max_val - min_val) * 100

    def _apply_conditional_logic(self, comps: Dict[str, float]) -> None:
        if comps['crime_index'] > 80 and comps['socioeconomic_level'] < 30:
            comps['crime_index'] *= 1.1

    def _apply_cross_feature(self, comps: Dict[str, float]) -> None:
        if comps['weather_condition'] > 70:
            comps['accident_rate'] *= 1.2

    def add_noise(self, score: float) -> float:
        return score + random.uniform(-self.noise_level, self.noise_level)

    def process(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        comps: Dict[str, float] = {}
        comps['crime_index'] = self._normalize(raw['crime_index'], 0, 10) * self.weights['crime_index']
        comps['accident_rate'] = self._normalize(raw['accident_rate'], 0, 10) * self.weights['accident_rate']
        comps['socioeconomic_level'] = self._normalize(raw['socioeconomic_level'], 1, 10) * self.weights[
            'socioeconomic_level']

        raw_weather = self.weights['weather_condition'][raw['weather_condition']]
        comps['weather_condition'] = self._normalize(raw_weather, 0, 10)

        self._apply_conditional_logic(comps)
        self._apply_cross_feature(comps)

        total = sum(comps.values())
        score = self.add_noise(total)
        return {'components': comps, 'risk_score': score}
