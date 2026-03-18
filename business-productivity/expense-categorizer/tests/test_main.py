import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
from main import cmd_categorize, cmd_check


def test_categorize_subcommand():
    with patch("sys.argv", ["main.py", "categorize"]):
        with patch("main.cmd_categorize") as mock_func:
            try:
                main()
            except SystemExit:
                pass

def test_check_subcommand():
    with patch("sys.argv", ["main.py", "check"]):
        with patch("main.cmd_check") as mock_func:
            try:
                main()
            except SystemExit:
                pass

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except SystemExit:
            pass
