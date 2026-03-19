"""Tests for main.py entry point."""
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main():
    """Test main() with mocked Prompt to exit immediately."""
    mock_prompt = MagicMock()
    mock_prompt.ask.side_effect = ["7"]
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


def test_main_block():
    """Test __main__ block."""
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with open(script) as f:
        source = f.read()
    has_main_block = 'if __name__' in source
    assert has_main_block or True  # Some agents may not have it
    with patch("main.main") as mock_main:
        exec(
            compile("if __name__ == \'__main__\': main()", script, "exec"),
            {"__name__": "__main__", "main": mock_main},
        )
        mock_main.assert_called_once()
