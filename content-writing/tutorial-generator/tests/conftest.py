import pytest
import sys
import os
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def mock_llm_response():
    return AIMessage(content="Mocked LLM Response")

@pytest.fixture
def mock_chat_openai(mocker, mock_llm_response):
    mock = mocker.patch("agent.generator.ChatOpenAI")
    instance = mock.return_value
    instance.invoke.return_value = mock_llm_response
    return instance
