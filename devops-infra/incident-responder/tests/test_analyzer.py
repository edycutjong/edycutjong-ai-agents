import pytest
from unittest.mock import MagicMock, patch
from agent.analyzer import LogAnalyzer

@pytest.fixture
def analyzer():
    return LogAnalyzer(api_key="sk-test")

@patch("agent.analyzer.ChatOpenAI")
def test_analyzer_init(mock_llm):
    analyzer = LogAnalyzer(api_key="sk-test")
    assert analyzer.llm

def test_analyze_logs_mock(analyzer):
    logs = [{"level": "ERROR", "message": "Test Error"}]

    # Mock the chain invocation
    analyzer.chain = MagicMock()
    analyzer.chain.invoke.return_value = {
        "anomalies": ["Test Error"],
        "root_cause": "Test Root Cause",
        "remediation": "Fix it",
        "severity": "HIGH",
        "summary": "Test Summary"
    }

    result = analyzer.analyze_logs(logs)

    assert result["severity"] == "HIGH"
    assert result["root_cause"] == "Test Root Cause"
    analyzer.chain.invoke.assert_called_once()
