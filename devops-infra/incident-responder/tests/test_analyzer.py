import pytest  # pragma: no cover
from unittest.mock import MagicMock, patch  # pragma: no cover
from agent.analyzer import LogAnalyzer  # pragma: no cover

@pytest.fixture  # pragma: no cover
def analyzer():  # pragma: no cover
    return LogAnalyzer(api_key="sk-test")  # pragma: no cover

@patch("agent.analyzer.ChatOpenAI")  # pragma: no cover
def test_analyzer_init(mock_llm):  # pragma: no cover
    analyzer = LogAnalyzer(api_key="sk-test")  # pragma: no cover
    assert analyzer.llm  # pragma: no cover

def test_analyze_logs_mock(analyzer):  # pragma: no cover
    logs = [{"level": "ERROR", "message": "Test Error"}]  # pragma: no cover

    # Mock the chain invocation
    analyzer.chain = MagicMock()  # pragma: no cover
    analyzer.chain.invoke.return_value = {  # pragma: no cover
        "anomalies": ["Test Error"],
        "root_cause": "Test Root Cause",
        "remediation": "Fix it",
        "severity": "HIGH",
        "summary": "Test Summary"
    }

    result = analyzer.analyze_logs(logs)  # pragma: no cover

    assert result["severity"] == "HIGH"  # pragma: no cover
    assert result["root_cause"] == "Test Root Cause"  # pragma: no cover
    analyzer.chain.invoke.assert_called_once()  # pragma: no cover
