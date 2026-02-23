import pytest
import sys
import os
from unittest.mock import MagicMock

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.debugger_agent import DebuggerAgent

def test_agent_initialization(mocker):
    mocker.patch("agent.debugger_agent.ChatOpenAI")
    agent = DebuggerAgent(api_key="sk-test")
    assert agent.llm is not None

def test_agent_missing_key(mocker):
    # Mock Config to ensure no env var
    mocker.patch("agent.debugger_agent.Config.OPENAI_API_KEY", None)

    agent = DebuggerAgent(api_key=None)
    assert agent.llm is None

    result = agent.analyze_error("Some error")
    assert "unavailable" in result

    result_config = agent.analyze_configuration("{}")
    assert "unavailable" in result_config
