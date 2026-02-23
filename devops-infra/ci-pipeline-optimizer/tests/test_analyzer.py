import pytest
from unittest.mock import MagicMock, patch
from agent.analyzer import CIAnalyzer

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    return llm

@pytest.fixture
def analyzer(mock_llm):
    analyzer = CIAnalyzer(mock_llm)
    # Mock the chain
    analyzer.analysis_chain = MagicMock()
    analyzer.analysis_chain.invoke.return_value = {
        "bottlenecks": ["Slow build"],
        "parallelization_opportunities": ["Run tests in parallel"],
        "caching_recommendations": ["Cache node_modules"],
        "other_improvements": ["Use smaller image"],
        "estimated_time_savings": "10 minutes"
    }
    return analyzer

def test_analyze_valid_yaml(analyzer):
    config = """
    name: CI
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - run: npm install
          - run: npm test
    """
    result = analyzer.analyze(config)

    assert "bottlenecks" in result
    assert result["bottlenecks"] == ["Slow build"]
    assert result["estimated_time_savings"] == "10 minutes"

def test_analyze_invalid_yaml(analyzer):
    config = """
    name: CI
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - run: npm install
          - run: npm test
      - invalid_indentation
    """
    result = analyzer.analyze(config)

    assert "error" in result
    assert "Invalid YAML configuration" in result["error"]

def test_analyze_llm_failure(analyzer):
    analyzer.analysis_chain.invoke.side_effect = Exception("API Error")
    config = """
    name: CI
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - run: echo hello
    """
    result = analyzer.analyze(config)

    assert "error" in result
    assert "Analysis failed" in result["error"]

def test_analyze_no_llm():
    analyzer = CIAnalyzer(None)
    assert analyzer.analysis_chain is None
    result = analyzer.analyze("config")
    assert "error" in result
    assert "LLM not initialized" in result["error"]
