import pytest
import os
from unittest.mock import patch
from config import Config

def test_config_validate_success():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test", "GEMINI_API_KEY": "test"}):
        config = Config()
        config.OPENAI_API_KEY = "test"
        config.GEMINI_API_KEY = "test"
        config.DEFAULT_PROVIDER = "openai"
        config.validate()  # Should not raise

def test_config_validate_openai_missing():
    with patch('config.Config.DEFAULT_PROVIDER', 'openai'):
        with patch('config.Config.OPENAI_API_KEY', None):
            with pytest.raises(ValueError, match="OPENAI_API_KEY is not set."):
                Config.validate()

def test_config_validate_google_missing():
    with patch('config.Config.DEFAULT_PROVIDER', 'google'):
        with patch('config.Config.GEMINI_API_KEY', None):
            with pytest.raises(ValueError, match="GEMINI_API_KEY is not set."):
                Config.validate()
