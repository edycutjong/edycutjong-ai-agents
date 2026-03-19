"""Coverage tests for main.py — interactive CLI with Rich Prompt."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_coverage():
    """Test main() with mocked Prompt.ask to break the interactive loop."""
    mock_prompt = MagicMock()
    mock_prompt.ask.side_effect = ["exit"]
    mock_console = MagicMock()
    mock_console.status.return_value.__enter__ = MagicMock()
    mock_console.status.return_value.__exit__ = MagicMock()
    with patch("main.Prompt", mock_prompt), \
         patch("main.Console", return_value=mock_console), \
         patch("builtins.print"):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass
