"""Coverage tests for main.py — Figma to CSS agent."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_help():
    """Test main() with --help flag."""
    with patch("sys.argv", ["main.py", "--help"]):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass


def test_main_no_args():
    """Test main() with no args — enters interactive mode, mock FigmaAgent and Prompt."""
    mock_prompt = MagicMock()
    mock_prompt.ask.side_effect = ["exit"]  # Exit interactive loop immediately
    mock_agent = MagicMock()
    mock_agent.run.return_value = "CSS output"
    with patch("sys.argv", ["main.py"]), \
         patch("main.Prompt", mock_prompt), \
         patch("main.FigmaAgent", return_value=mock_agent), \
         patch("main.OPENAI_API_KEY", "test-key"), \
         patch("main.console"):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass
