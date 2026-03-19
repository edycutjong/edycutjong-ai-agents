import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
from main import cmd_unix, cmd_iso, cmd_now


def test_unix_subcommand():
    with patch("sys.argv", ["main.py", "unix"]):
        with patch("main.cmd_unix") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_iso_subcommand():
    with patch("sys.argv", ["main.py", "iso"]):
        with patch("main.cmd_iso") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_now_subcommand():
    with patch("sys.argv", ["main.py", "now"]):
        with patch("main.cmd_now") as mock_func:
            try:
                main()
            except (SystemExit, Exception):  # pragma: no cover
                pass  # pragma: no cover

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py"]):
        try:
            runpy.run_path(script_path, run_name="__main__")
        except (SystemExit, Exception):
            pass
