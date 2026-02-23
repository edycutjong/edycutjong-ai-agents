import pytest
from unittest.mock import MagicMock, patch
from agent.ci_agent import CIAgent

@pytest.fixture
def mock_llm():
    return MagicMock()

@patch('agent.ci_agent.ChatOpenAI')
def test_ci_agent_init(MockChatOpenAI, mock_llm):
    MockChatOpenAI.return_value = mock_llm

    agent = CIAgent(api_key="sk-test")
    assert agent.analyzer is not None
    assert agent.optimizer is not None
    assert agent.llm is mock_llm

    # Verify methods delegate
    agent.analyzer.analyze = MagicMock(return_value={"status": "ok"})
    agent.optimizer.optimize = MagicMock(return_value="optimized")

    res = agent.analyze("yaml")
    assert res["status"] == "ok"
    agent.analyzer.analyze.assert_called_once()

    res = agent.optimize("yaml", {})
    assert res == "optimized"
    agent.optimizer.optimize.assert_called_once()

def test_ci_agent_no_key():
    # Mock Config
    with pytest.MonkeyPatch.context() as m:
        m.setattr("config.Config.OPENAI_API_KEY", None)
        agent = CIAgent(api_key=None)
        assert agent.llm is None
        assert agent.analyzer.analysis_chain is None
        assert agent.optimizer.optimization_chain is None
