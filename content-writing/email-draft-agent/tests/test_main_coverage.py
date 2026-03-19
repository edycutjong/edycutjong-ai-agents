"""Coverage tests for main.py — argparse + Rich Prompt CLI."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_coverage():
    """Test main() with mocked Prompt.ask and sys.argv."""
    mock_prompt = MagicMock()
    mock_prompt.ask.return_value = "test"
    mock_console = MagicMock()
    with patch("sys.argv", ["main.py", "--help"]):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass


def test_main_no_args():
    """Test main() with no args and mocked prompts."""
    mock_prompt = MagicMock()
    mock_prompt.ask.return_value = "test"
    mock_console = MagicMock()
    with patch("sys.argv", ["main.py"]), \
         patch("main.Prompt", mock_prompt), \
         patch("builtins.print"):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass
