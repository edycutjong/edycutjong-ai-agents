import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage
import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.core import create_agent_executor, run_agent_step

@patch("agent.core.get_llm")
@patch("agent.core.create_react_agent")
def test_create_agent_executor(mock_create_react_agent, mock_get_llm):
    mock_llm = MagicMock()
    mock_get_llm.return_value = mock_llm

    mock_agent = MagicMock()
    mock_create_react_agent.return_value = mock_agent

    executor = create_agent_executor()

    assert executor == mock_agent
    mock_get_llm.assert_called_once()
    mock_create_react_agent.assert_called_once()

@patch("agent.core.get_llm")
def test_create_agent_executor_no_key(mock_get_llm):
    mock_get_llm.return_value = None
    executor = create_agent_executor()
    assert executor is None

def test_run_agent_step_success():
    mock_executor = MagicMock()
    # Mock return value of invoke. It returns a dict with 'messages' list.
    # The last message is the response content.
    ai_message = MagicMock()
    ai_message.content = "Hello!"
    mock_response = {"messages": [HumanMessage(content="Hi"), ai_message]}
    mock_executor.invoke.return_value = mock_response

    response = run_agent_step(mock_executor, "Hi", thread_id="test")

    assert response == "Hello!"
    mock_executor.invoke.assert_called_once()
    # Check arguments passed to invoke
    args, kwargs = mock_executor.invoke.call_args
    assert len(args[0]['messages']) == 1
    assert args[0]['messages'][0].content == "Hi"
    assert kwargs['config']['configurable']['thread_id'] == "test"

def test_run_agent_step_error():
    mock_executor = MagicMock()
    mock_executor.invoke.side_effect = Exception("Test error")

    response = run_agent_step(mock_executor, "Hi")
    assert "Error running agent: Test error" in response

def test_run_agent_step_not_initialized():
    response = run_agent_step(None, "Hi")
    assert "Agent not initialized" in response
