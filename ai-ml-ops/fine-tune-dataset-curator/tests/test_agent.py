import pytest
from unittest.mock import patch, MagicMock
from agent.curator import create_curator_agent
from config import Config

# Mock Config
@pytest.fixture
def mock_config(monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_API_KEY", "sk-fake-key")

def test_agent_initialization(mock_config):
    # Mock ChatOpenAI to avoid actual API calls
    with patch("agent.curator.ChatOpenAI") as mock_llm:
        agent_executor = create_curator_agent()
        assert agent_executor is not None
        assert mock_llm.called

def test_agent_invocation_failure_without_key(monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_API_KEY", None)
    # create_curator_agent uses Config.OPENAI_API_KEY directly in call to ChatOpenAI
    # which might fail if the library validates it immediately, or pass until invocation.
    # However, ChatOpenAI usually requires api_key.

    # We expect failure or error if key is missing when we try to init.
    # Actually, ChatOpenAI might raise validation error.
    with pytest.raises(Exception):
        # We need to ensure the Config.OPENAI_API_KEY is actually None when accessed
        create_curator_agent()
