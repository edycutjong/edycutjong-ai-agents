import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

@patch('main.Crew')
@patch('main.get_commits')
@patch('main.Prompt.ask')
@patch('main.console.print') # Mock rich console output
@patch('main.console.status') # Mock rich status
@patch.dict(os.environ, {"OPENAI_API_KEY": "dummy"})
def test_main(mock_status, mock_print, mock_ask, mock_get_commits, mock_crew_class):
    # Mock user input
    mock_ask.side_effect = ["/path/to/repo", "HEAD~5", "HEAD"]

    # Mock status context manager
    mock_status.return_value.__enter__.return_value = MagicMock()

    # Mock git commits
    mock_get_commits.return_value = [{
        "hash": "abc", "author": "me", "date": "today", "message": "feat: test", "files_changed": []
    }]

    # Mock Crew execution
    mock_crew = MagicMock()
    mock_crew_class.return_value = mock_crew
    mock_crew.kickoff.return_value = "# Changelog\n\n- feat: test"

    # Run main
    main.main()

    # Assertions
    mock_get_commits.assert_called_with("/path/to/repo", "HEAD~5", "HEAD")
    mock_crew.kickoff.assert_called_once()

    # Verify file creation
    assert os.path.exists("CHANGELOG.md")
    with open("CHANGELOG.md", "r") as f:
        content = f.read()
        assert "feat: test" in content

    # Cleanup
    os.remove("CHANGELOG.md")
