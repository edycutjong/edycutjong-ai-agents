import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from agent.core import TravelAgent

@pytest.fixture
def mock_agent_executor(mocker):
    executor = MagicMock()
    # Mock invoke return value structure for LangGraph
    executor.invoke.return_value = {"messages": [AIMessage(content="Mocked Itinerary")]}
    return executor

def test_travel_agent_init_mock(mocker):
    mocker.patch("agent.core.OPENAI_API_KEY", "mock-key")
    mocker.patch("agent.core.ChatOpenAI", MagicMock())
    mocker.patch("agent.core.create_react_agent", MagicMock())

    agent = TravelAgent()
    assert agent.agent_executor is not None

def test_travel_agent_generate_itinerary(mocker, mock_agent_executor):
    mocker.patch("agent.core.OPENAI_API_KEY", "mock-key")
    mocker.patch("agent.core.ChatOpenAI", MagicMock())
    mocker.patch("agent.core.create_react_agent", return_value=mock_agent_executor)

    agent = TravelAgent()
    itinerary = agent.generate_itinerary("Paris", "May 1-5")
    assert itinerary == "Mocked Itinerary"
    mock_agent_executor.invoke.assert_called_once()

def test_travel_agent_no_key(mocker):
    mocker.patch("agent.core.OPENAI_API_KEY", None)

    agent = TravelAgent()
    assert agent.agent_executor is None
    result = agent.generate_itinerary("Paris", "May 1-5")
    assert "Error: OPENAI_API_KEY not found" in result
