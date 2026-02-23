import pytest
import os
from unittest.mock import patch, MagicMock
from agent.ai_editor import AIEditor

def test_ai_polish_mock():
    with patch("agent.ai_editor.ChatOpenAI") as MockChat:
        mock_llm = MockChat.return_value
        mock_llm.invoke.return_value.content = "Polished Content"

        editor = AIEditor(api_key="fake")
        res = editor.polish_content("Raw Content")

        assert res == "Polished Content"
        mock_llm.invoke.assert_called_once()

def test_ai_no_key():
    # Ensure OPENAI_API_KEY is not set
    with patch.dict('os.environ', {}, clear=True):
        editor = AIEditor(api_key=None)
        res = editor.polish_content("Raw")
        assert res == "Raw"

def test_empty_content():
    editor = AIEditor(api_key="fake")
    res = editor.polish_content("")
    assert res == ""
