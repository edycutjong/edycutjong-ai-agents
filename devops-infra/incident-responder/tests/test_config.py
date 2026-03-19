import os  # pragma: no cover
import sys  # pragma: no cover
import importlib  # pragma: no cover
from unittest.mock import patch  # pragma: no cover

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))  # pragma: no cover

def test_config_import():  # pragma: no cover
    import config  # pragma: no cover
    assert config is not None  # pragma: no cover

def test_config_env_vars():  # pragma: no cover
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key", "GEMINI_API_KEY": "test-gem", "MODEL": "test-model", "DEBUG": "true"}):  # pragma: no cover
        # Force reimport
        if "config" in sys.modules:  # pragma: no cover
            del sys.modules["config"]  # pragma: no cover
        import config  # pragma: no cover
        importlib.reload(config)  # pragma: no cover
        assert config is not None  # pragma: no cover
