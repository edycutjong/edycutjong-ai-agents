from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent import main

@patch("agent.Prompt.ask")
@patch("agent.console")
@patch("agent.ask_user")
@patch("agent.spinner")
@patch("tools.checker.StyleChecker.scan_directory")
def test_main_scan_flow(mock_scan, mock_spinner, mock_ask_user, mock_console, mock_prompt):
    # Setup mocks
    mock_prompt.side_effect = ["scan", "quit"] # First scan, then quit
    mock_ask_user.side_effect = [".", "n"] # Scan path '.', then 'n' for explanation
    mock_scan.return_value = [{"path": "foo.py", "row": 1, "col": 1, "code": "E123", "text": "bad code"}]

    # Run main
    try:
        main()
    except SystemExit:
        pass

    # Assertions
    mock_prompt.assert_called()
    mock_ask_user.assert_called()
    mock_scan.assert_called_with(".")
    mock_console.print.assert_called()

@patch("agent.Prompt.ask")
@patch("agent.console")
def test_main_quit(mock_console, mock_prompt):
    mock_prompt.return_value = "quit"
    try:
        main()
    except SystemExit:
        pass
    mock_prompt.assert_called_once()
