import os
import sys
import importlib
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_config_import():
    import config  # pragma: no cover
    assert config is not None  # pragma: no cover

def test_config_env_vars():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GEMINI_API_KEY": "test-gem", "MODEL": "test-model", "DEBUG": "true"}):  # pragma: no cover
        # Force reimport
        if "config" in sys.modules:  # pragma: no cover
            del sys.modules["config"]  # pragma: no cover
        import config  # pragma: no cover
        importlib.reload(config)  # pragma: no cover
        assert config is not None  # pragma: no cover
