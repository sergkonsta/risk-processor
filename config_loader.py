import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent
        self.path = base_dir / 'config' / 'config.yaml'
        self._config = None

    def load(self) -> dict:
        if self._config is None:
            with self.path.open('r') as f:
                self._config = yaml.safe_load(f)
        return self._config