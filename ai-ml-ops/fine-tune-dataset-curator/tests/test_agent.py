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

@patch('agent.curator.ChatOpenAI')
def test_agent_invocation_without_key(mock_llm, monkeypatch):
    monkeypatch.setattr(Config, "OPENAI_API_KEY", None)
    mock_llm.side_effect = Exception("Missing API key")
    
    with pytest.raises(Exception, match="Missing API key"):
        create_curator_agent()
