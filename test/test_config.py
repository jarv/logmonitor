import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from config import config_from_yaml  # noqa: E731


def test_config():
    y = config_from_yaml()
    assert isinstance(y, dict)
