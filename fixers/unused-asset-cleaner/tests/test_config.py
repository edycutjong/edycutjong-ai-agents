import os
import sys
import importlib
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_config_import():
    import config
    assert config is not None
