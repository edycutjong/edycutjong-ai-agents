import pytest
from config import Config

def test_config_valid(monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_API_KEY", "dummy")
    # Should not raise
    Config.validate()
    
def test_config_invalid(monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_API_KEY", None)
    with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is not set"):
        Config.validate()
