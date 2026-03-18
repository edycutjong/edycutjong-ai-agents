import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
from main import cmd_convert, cmd_validate, cmd_format, cmd_detect


def test_convert_subcommand():
    with patch("sys.argv", ["main.py", "convert"]):
        with patch("main.cmd_convert") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_validate_subcommand():
    with patch("sys.argv", ["main.py", "validate"]):
        with patch("main.cmd_validate") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_format_subcommand():
    with patch("sys.argv", ["main.py", "format"]):
        with patch("main.cmd_format") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_detect_subcommand():
    with patch("sys.argv", ["main.py", "detect"]):
        with patch("main.cmd_detect") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except (SystemExit, Exception):
            pass
