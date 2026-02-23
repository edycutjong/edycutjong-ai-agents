import pytest
from unittest.mock import MagicMock, patch
from agent.llm import LLMAnalyzer
import pandas as pd
import json

def test_analyze_report_no_key():
    # Ensure no API key in env
    with patch.dict('os.environ', {'OPENAI_API_KEY': ''}):
        analyzer = LLMAnalyzer(api_key=None)
        result = analyzer.analyze_report({})
        assert "No OpenAI API Key" in result

def test_analyze_report_with_key():
    # Mock ChatOpenAI to avoid real init
    with patch('agent.llm.ChatOpenAI') as MockChat:
        mock_llm = MockChat.return_value

        # Mock response object
        mock_response = MagicMock()
        mock_response.content = "Analysis Summary"

        # Configure the mock to return this response when invoked
        # LangChain RunnableSequence calls invoke()
        mock_llm.invoke.return_value = mock_response
        # Just in case it calls __call__
        mock_llm.return_value = mock_response

        analyzer = LLMAnalyzer(api_key="fake-key")

        report = {"test": "data"}
        result = analyzer.analyze_report(report)

        # If result is still a mock, we know the chain isn't using our configured method.
        # But assuming it works:
        if isinstance(result, MagicMock):
             # Fallback debug: if it returns a mock, it means our config wasn't used.
             # We can't print easily here.
             pass

        assert result == "Analysis Summary"

def test_verify_transformation_no_rule():
    with patch('agent.llm.ChatOpenAI'):
        analyzer = LLMAnalyzer(api_key="fake-key")
        result = analyzer.verify_transformation(pd.DataFrame(), pd.DataFrame(), "")
        assert "No transformation rule provided" in result
