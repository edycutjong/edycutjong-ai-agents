import pytest
from unittest.mock import MagicMock
from agent.optimizer import CIOptimizer

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    return llm

@pytest.fixture
def optimizer(mock_llm):
    optimizer = CIOptimizer(mock_llm)
    optimizer.optimization_chain = MagicMock()
    optimizer.optimization_chain.invoke.return_value = """
    name: CI Optimized
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            node: [14, 16]
        steps:
          - uses: actions/checkout@v2
          - uses: actions/setup-node@v2
            with:
              node-version: ${{ matrix.node }}
              cache: 'npm'
          - run: npm install
          - run: npm test
    """
    return optimizer

def test_optimize_valid_yaml(optimizer):
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
    analysis_result = {
        "bottlenecks": ["Slow build"],
        "parallelization_opportunities": ["Run tests in parallel"],
        "caching_recommendations": ["Cache node_modules"],
        "other_improvements": ["Use smaller image"],
        "estimated_time_savings": "10 minutes"
    }

    result = optimizer.optimize(config, analysis_result)

    assert "name: CI Optimized" in result
    assert "cache: 'npm'" in result

def test_optimize_llm_failure(optimizer):
    optimizer.optimization_chain.invoke.side_effect = Exception("API Error")
    config = """
    name: CI
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - run: echo hello
    """
    analysis_result = {"bottlenecks": ["Slow build"]}

    result = optimizer.optimize(config, analysis_result)

    assert "# Optimization failed" in result

def test_optimize_markdown_stripping(optimizer):
    # Mock LLM returning markdown
    optimizer.optimization_chain.invoke.return_value = """
    ```yaml
    name: CI Optimized
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - run: echo hello
    ```
    """
    config = """
    name: CI
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - run: echo hello
    """
    analysis_result = {"bottlenecks": ["Slow build"]}

    result = optimizer.optimize(config, analysis_result)

    assert result.startswith("name: CI Optimized")
    assert not result.startswith("```yaml")

def test_optimize_no_llm():
    optimizer = CIOptimizer(None)
    assert optimizer.optimization_chain is None
    result = optimizer.optimize("config", {})
    assert "Optimization failed" in result
    assert "LLM not initialized" in result

def test_optimize_analysis_string(optimizer):
    # Test when analysis result is a string
    config = "config"
    analysis_result = "Some string analysis"
    optimizer.optimize(config, analysis_result)
    optimizer.optimization_chain.invoke.assert_called_with({
        "config_content": config,
        "analysis": analysis_result
    })
