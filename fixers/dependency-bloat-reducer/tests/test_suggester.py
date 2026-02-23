import os
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage
from tools.suggester import SuggestionEngine

@pytest.fixture
def mock_llm_chain():
    with patch("tools.suggester.ChatOpenAI") as MockChatOpenAI:
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = AIMessage(content="- Suggestion 1\n- Suggestion 2")
        mock_llm_instance.return_value = AIMessage(content="- Suggestion 1\n- Suggestion 2")
        MockChatOpenAI.return_value = mock_llm_instance
        yield MockChatOpenAI

def test_suggester_with_key(mock_llm_chain):
    suggester = SuggestionEngine(api_key="fake-key")
    dependency_sizes = [{"name": "react", "size": 1024}]
    unused_deps = ["lodash"]

    suggestions = suggester.get_suggestions(dependency_sizes, unused_deps)
    assert len(suggestions) > 0
    assert "Suggestion 1" in suggestions[0]

def test_suggester_without_key():
    # Unset env var if set
    with patch.dict(os.environ, {}, clear=True):
        suggester = SuggestionEngine(api_key=None)
        suggestions = suggester.get_suggestions([], [])
        assert "AI suggestions unavailable" in suggestions[0]
