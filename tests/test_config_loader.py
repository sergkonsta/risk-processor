import yaml
import pytest
from config_loader import ConfigLoader


def test_load_default_path():
    expected_config = {
        'risk': {'noise_level': 2.0}
    }
    cfg = ConfigLoader().load()
    assert expected_config['risk']['noise_level'] == cfg['risk']['noise_level']