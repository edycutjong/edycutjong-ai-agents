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
    with patch('config.config.GEMINI_API_KEY', 'test_key'):
        generator = AltTextGenerator(provider='google')
        result = generator.generate_alt_text("base64data", "context")
        assert result == "A Google descriptive alt text."
        mock_llm_google.return_value.invoke.assert_called_once()

import asyncio

@pytest.fixture
def mock_llm_openai_async():
    with patch('agent.generator.ChatOpenAI') as mock:
        llm_instance = MagicMock()

        async def mock_ainvoke(*args, **kwargs):
            return AIMessage(content="Async descriptive alt text.")

        llm_instance.ainvoke = mock_ainvoke
        mock.return_value = llm_instance
        yield mock

@pytest.mark.asyncio
async def test_generate_alt_text_async_openai(mock_llm_openai_async):
    with patch('config.config.OPENAI_API_KEY', 'test_key'):
        generator = AltTextGenerator(provider='openai')
        result = await generator.generate_alt_text_async("base64data", "context")
        assert result == "Async descriptive alt text."
