import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.generator import AltTextGenerator
from langchain_core.messages import AIMessage

@pytest.fixture
def mock_llm_openai():
    with patch('agent.generator.ChatOpenAI') as mock:
        llm_instance = MagicMock()
        llm_instance.invoke.return_value = AIMessage(content="A descriptive alt text.")
        mock.return_value = llm_instance
        yield mock

@pytest.fixture
def mock_llm_google():
    with patch('agent.generator.ChatGoogleGenerativeAI') as mock:
        llm_instance = MagicMock()
        llm_instance.invoke.return_value = AIMessage(content="A Google descriptive alt text.")
        mock.return_value = llm_instance
        yield mock

def test_generate_alt_text_openai(mock_llm_openai):
    with patch('config.config.OPENAI_API_KEY', 'test_key'):
        generator = AltTextGenerator(provider='openai')
        result = generator.generate_alt_text("base64data", "context")
        assert result == "A descriptive alt text."
        mock_llm_openai.return_value.invoke.assert_called_once()

def test_generate_alt_text_google(mock_llm_google):
    with patch('config.config.GOOGLE_API_KEY', 'test_key'):
        generator = AltTextGenerator(provider='google')
        result = generator.generate_alt_text("base64data", "context")
        assert result == "A Google descriptive alt text."
        mock_llm_google.return_value.invoke.assert_called_once()
