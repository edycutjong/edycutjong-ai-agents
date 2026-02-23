import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_config import CalendarTool, SaveDraftTool
from email_processor import EmailDrafter

def test_calendar_tool():
    tool = CalendarTool()
    assert tool.name == "check_calendar"

    # Test specific dates based on mock logic
    assert "Busy" in tool._run("2023-10-25")
    assert "Free all day" in tool._run("2023-10-26")
    assert "Free" in tool._run("2023-10-27")

def test_save_draft_tool(tmp_path):
    tool = SaveDraftTool()
    assert tool.name == "save_draft"

    # Change working directory to tmp_path for file creation test
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = tool._run("This is a draft", "John Doe")
        assert "Draft saved to" in result

        expected_file = "draft_to_John_Doe.txt"
        assert os.path.exists(expected_file)

        with open(expected_file, "r") as f:
            content = f.read()
        assert content == "This is a draft"
    finally:
        os.chdir(original_cwd)

@patch('email_processor.get_llm')
@patch('email_processor.create_react_agent')
def test_email_drafter(mock_create_react_agent, mock_get_llm):
    # Setup mocks
    mock_agent_instance = MagicMock()
    mock_create_react_agent.return_value = mock_agent_instance

    # Mock invoke response
    mock_message = MagicMock()
    mock_message.content = "Here is the drafted email."
    mock_agent_instance.invoke.return_value = {"messages": [MagicMock(), mock_message]}

    drafter = EmailDrafter()

    response = drafter.draft_email("Hello, can we meet?")

    assert response == "Here is the drafted email."
    mock_agent_instance.invoke.assert_called_once()
    args, kwargs = mock_agent_instance.invoke.call_args
    assert "Draft a response" in args[0]['messages'][0][1]
