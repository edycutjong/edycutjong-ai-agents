import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test fallback for missing config
with patch.dict('sys.modules', {'config': None}):
    import agent.analysis
    import importlib
    importlib.reload(agent.analysis)

from agent.analysis import analyze_failure

@patch('agent.analysis.ChatOpenAI')
@patch('agent.analysis.ChatPromptTemplate')
def test_analyze_failure(mock_prompt_template, mock_chat_openai):
    mock_llm = MagicMock()
    mock_chat_openai.return_value = mock_llm
    mock_prompt = MagicMock()
    mock_prompt_template.from_messages.return_value = mock_prompt
    mock_chain = MagicMock()
    mock_prompt.__or__.return_value = mock_chain
    mock_chain.invoke.return_value.content = "Diagnosis: Check your DNS."

    with patch('agent.analysis.OPENAI_API_KEY', 'fake-key'):
        diagnosis = analyze_failure("http://example.com", 500, 0.1, "Internal Server Error")
        assert diagnosis == "Diagnosis: Check your DNS."
        mock_prompt.__or__.assert_called()
        mock_chain.invoke.assert_called_once()
        
        # Test exception
        mock_chain.invoke.side_effect = Exception("LLM Error")
        assert "AI Diagnosis failed" in analyze_failure("url", 500, 0.1, "err")

def test_analyze_failure_no_key():
    with patch('agent.analysis.OPENAI_API_KEY', None):
        diagnosis = analyze_failure("http://example.com", 500, 0.1, "Internal Server Error")
        assert "not configured" in diagnosis
