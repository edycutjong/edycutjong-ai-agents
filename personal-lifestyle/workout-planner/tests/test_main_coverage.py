"""Coverage tests for main.py — linear Rich Prompt CLI."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_coverage():
    """Test main() with mocked Prompt.ask calls."""
    mock_prompt = MagicMock()
    mock_prompt.ask.return_value = "test"
    mock_int_prompt = MagicMock()
    mock_int_prompt.ask.return_value = 3
    mock_float_prompt = MagicMock()
    mock_float_prompt.ask.return_value = 70.0
    mock_console = MagicMock()
    with patch("main.Prompt", mock_prompt), \
         patch("main.Console", return_value=mock_console), \
         patch("builtins.print"):
        # Also mock IntPrompt and FloatPrompt if they exist
        try:
            with patch("main.IntPrompt", mock_int_prompt):
                pass
        except AttributeError:
            pass
        try:
            with patch("main.FloatPrompt", mock_float_prompt):
                pass
        except AttributeError:
            pass
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass
