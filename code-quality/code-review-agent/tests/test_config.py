import os
import sys
import importlib
import pytest


import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_builtin_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "dummy")


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_config_import():
    import config
    assert config is not None

def test_config_class():
    import config
    c = config.Config()
    assert c is not None

def test_config_env_vars():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GEMINI_API_KEY": "test-gem", "MODEL": "test-model", "DEBUG": "true"}):
        # Force reimport
        if "config" in sys.modules:
            del sys.modules["config"]
        import config
        importlib.reload(config)
        assert config.Config is not None
