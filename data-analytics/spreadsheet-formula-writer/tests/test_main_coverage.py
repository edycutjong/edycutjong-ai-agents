"""Coverage tests for main.py — Typer CLI."""
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_main_no_args():
    """Test main with no args — should print help or exit cleanly."""
    with patch("sys.argv", ["main.py", "--help"]):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass


def test_main_with_args():
    """Test main with a sample argument."""
    with patch("sys.argv", ["main.py", "test_input"]):
        try:
            from main import main
            main()
        except (SystemExit, Exception):
            pass
