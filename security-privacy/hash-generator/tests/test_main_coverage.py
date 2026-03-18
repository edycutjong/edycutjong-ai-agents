import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
from main import cmd_hash, cmd_multi


def test_hash_subcommand():
    with patch("sys.argv", ["main.py", "hash"]):
        with patch("main.cmd_hash") as mock_func:
            try:
                main()
            except SystemExit:
                pass

def test_multi_subcommand():
    with patch("sys.argv", ["main.py", "multi"]):
        with patch("main.cmd_multi") as mock_func:
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
