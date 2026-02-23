import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.analysis import analyze_failure

@patch('agent.analysis.ChatOpenAI')
@patch('agent.analysis.ChatPromptTemplate')
def test_analyze_failure(mock_prompt_template, mock_chat_openai):
    # Mock LLM
    mock_llm = MagicMock()
    mock_chat_openai.return_value = mock_llm

    # Mock Prompt
    mock_prompt = MagicMock()
    mock_prompt_template.from_messages.return_value = mock_prompt

    # Mock Chain (prompt | llm)
    mock_chain = MagicMock()
    # Mock the pipe operator
    mock_prompt.__or__.return_value = mock_chain
    mock_chain.invoke.return_value.content = "Diagnosis: Check your DNS."

    # Mock OPENAI_API_KEY
    with patch('agent.analysis.OPENAI_API_KEY', 'fake-key'):
        diagnosis = analyze_failure("http://example.com", 500, 0.1, "Internal Server Error")

        # Verify result
        assert diagnosis == "Diagnosis: Check your DNS."

        # Verify chain execution
        # Check that prompt | llm was called
        mock_prompt.__or__.assert_called()
        mock_chain.invoke.assert_called_once()

def test_analyze_failure_no_key():
    # We need to ensure OPENAI_API_KEY is None during import or patched.
    # Since it's imported at module level, patching agent.analysis.OPENAI_API_KEY works.
    with patch('agent.analysis.OPENAI_API_KEY', None):
        diagnosis = analyze_failure("http://example.com", 500, 0.1, "Internal Server Error")
        assert "not configured" in diagnosis
