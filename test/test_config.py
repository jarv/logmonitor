from config import config_from_yaml


def test_config():
    y = config_from_yaml()
    assert isinstance(y, dict)
