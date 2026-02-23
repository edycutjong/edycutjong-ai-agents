import pytest
from unittest.mock import patch, Mock
import os
from agent.analyst import KPIAnalyst

def test_analyze_dashboard_no_key():
    # Ensure OPENAI_API_KEY is not set for this test
    with patch.dict('os.environ', {}, clear=True):
        analyst = KPIAnalyst(api_key=None)
        res = analyst.analyze_dashboard("test")
        assert "not configured" in res

def test_analyze_dashboard_mock_llm():
    with patch('agent.analyst.ChatOpenAI') as MockLLM:
        mock_instance = MockLLM.return_value
        mock_instance.invoke.return_value = Mock(content="Executive Summary")

        analyst = KPIAnalyst(api_key="fake-key")
        res = analyst.analyze_dashboard("data summary")
        assert res == "Executive Summary"
