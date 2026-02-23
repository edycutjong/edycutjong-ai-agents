import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add app directory to path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from agent.analysis import ContentAnalyzer
from langchain_core.messages import AIMessage

@patch("agent.analysis.ChatOpenAI")
def test_summarize(mock_chat_openai):
    # Setup mock
    mock_llm_instance = MagicMock()
    mock_chat_openai.return_value = mock_llm_instance

    # When using LCEL pipe | with a Mock, the Mock is treated as a callable in the sequence.
    # So it calls mock_llm_instance(...) directly, not .invoke()
    mock_llm_instance.return_value = AIMessage(content="Summary Result")

    analyzer = ContentAnalyzer(api_key="test_key")

    result = analyzer.summarize("Transcript text")

    assert result == "Summary Result"
    # Verify it was called (either as callable or invoke, depending on how LCEL wraps it)
    # Since it's a mock, it likely just got called.
    assert mock_llm_instance.called

@patch("agent.analysis.ChatOpenAI")
def test_generate_chapters(mock_chat_openai):
    # Setup mock
    mock_llm_instance = MagicMock()
    mock_chat_openai.return_value = mock_llm_instance

    mock_llm_instance.return_value = AIMessage(content="Chapters Result")

    analyzer = ContentAnalyzer(api_key="test_key")

    result = analyzer.generate_chapters("Transcript text")

    assert result == "Chapters Result"
    assert mock_llm_instance.called

def test_analysis_no_api_key():
    with pytest.raises(ValueError):
        ContentAnalyzer(api_key="")
