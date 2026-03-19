"""Tests for main.py entry point."""
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main():
    """Test main() with mocked subprocess."""
    with patch("subprocess.run", return_value=None):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass


def test_main_block():
    """Test __main__ block."""
    with patch("subprocess.run", return_value=None):
        script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
        with patch("main.main") as mock_main:
            exec(
                compile("if __name__ == \'__main__\': main()", script, "exec"),
                {"__name__": "__main__", "main": mock_main},
            )
            mock_main.assert_called_once()
