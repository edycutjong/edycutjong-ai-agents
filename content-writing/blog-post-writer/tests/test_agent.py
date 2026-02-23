import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Ensure the app directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent.researcher import Researcher
from agent.writer import Writer
from agent.seo import SEOOptimizer
from agent.utils import clean_text, format_filename

@pytest.fixture
def mock_llm_response():
    mock = MagicMock()
    mock.invoke.return_value.content = "Mocked Response"
    return mock

@patch("agent.researcher.DuckDuckGoSearchRun")
@patch("agent.researcher.ChatOpenAI")
def test_researcher(mock_chat, mock_search):
    # Setup mocks
    mock_search_instance = mock_search.return_value
    mock_search_instance.run.return_value = "Search Results"

    mock_llm = mock_chat.return_value
    mock_llm.invoke.return_value.content = "Research Summary"

    # Test
    researcher = Researcher()
    result = researcher.research("Test Topic")

    assert result["topic"] == "Test Topic"
    assert result["raw_search_results"] == "Search Results"
    # Note: Because of how LCEL works, mocking might be tricky if the chain is composed in __init__
    # However, since we mock ChatOpenAI which is part of the chain, it should work if we mock the invoke method on the chain or the llm.
    # But wait, `self.summary_chain = RESEARCH_SUMMARY_PROMPT | self.llm`
    # So `self.summary_chain.invoke` calls `RESEARCH_SUMMARY_PROMPT.invoke` then `self.llm.invoke`.
    # Mocking `self.llm.invoke` should work.

    # Actually, we need to mock the chain execution.
    # But let's see if the mock on ChatOpenAI propagates.
    # If LLM is part of the chain, the chain calls llm.invoke().
    # So mocking llm.invoke() works.

    # Wait, `self.llm` is instantiated inside `__init__`.
    # `mock_chat` patches the class `ChatOpenAI`.
    # So `self.llm` is `mock_chat.return_value`.
    # So `self.llm.invoke` is mocked.

    # However, `RESEARCH_SUMMARY_PROMPT | self.llm` creates a RunnableSequence.
    # When `summary_chain.invoke` is called, it runs the prompt then the LLM.
    # So `self.llm.invoke` (or `__call__` or `predict` depending on version) is called.
    # In newer LangChain, `invoke` is standard.

    # Let's assume the mock return value.
    # Since I'm mocking the class, the instance will be a mock.
    # But does `RESEARCH_SUMMARY_PROMPT | mock_instance` work? Yes, mocks are flexible.

    # But the return value of the chain.invoke() is what matters.
    # If the chain returns the mock's return value, that's fine.
    # But the prompt returns a prompt value (string or messages).
    # Then the LLM (mock) is called with that prompt value.
    # So `mock_llm.invoke.return_value` should be the final result.
    # The result of `llm.invoke()` is usually an AIMessage object.
    # So `mock_llm.invoke.return_value` should have a `.content` attribute.

    mock_message = MagicMock()
    mock_message.content = "Research Summary"
    # Mock both invoke and __call__ to be safe
    mock_llm.invoke.return_value = mock_message
    mock_llm.return_value = mock_message

    # Re-run because setup was modified
    researcher = Researcher()

    result = researcher.research("Test Topic")
    assert result["summary"] == "Research Summary"

@patch("agent.writer.ChatOpenAI")
def test_writer(mock_chat):
    mock_llm = mock_chat.return_value
    mock_message = MagicMock()
    mock_message.content = "Generated Content"
    mock_llm.invoke.return_value = mock_message
    mock_llm.return_value = mock_message

    writer = Writer()
    outline = writer.create_outline("Topic", "Summary")
    assert outline == "Generated Content"

    post = writer.write_post("Topic", "Outline", "Summary")
    assert post == "Generated Content"

@patch("agent.seo.ChatOpenAI")
def test_seo(mock_chat):
    mock_llm = mock_chat.return_value
    mock_message = MagicMock()
    mock_message.content = "SEO Report"
    mock_llm.invoke.return_value = mock_message
    mock_llm.return_value = mock_message

    optimizer = SEOOptimizer()
    result = optimizer.optimize("Topic", "Content")

    assert result["seo_report"] == "SEO Report"

def test_utils():
    assert clean_text("  hello   world  ") == "hello world"
    assert format_filename("Hello World!") == "hello-world"
