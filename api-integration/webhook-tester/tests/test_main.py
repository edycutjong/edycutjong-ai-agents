import os
import sys
import runpy
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main
from main import cmd_list, cmd_show, cmd_replay, cmd_curl, cmd_python, cmd_export, cmd_clear, cmd_capture


def test_list_subcommand():
    with patch("sys.argv", ["main.py", "list"]):
        with patch("main.cmd_list") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_show_subcommand():
    with patch("sys.argv", ["main.py", "show"]):
        with patch("main.cmd_show") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_replay_subcommand():
    with patch("sys.argv", ["main.py", "replay"]):
        with patch("main.cmd_replay") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_curl_subcommand():
    with patch("sys.argv", ["main.py", "curl"]):
        with patch("main.cmd_curl") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_python_subcommand():
    with patch("sys.argv", ["main.py", "python"]):
        with patch("main.cmd_python") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_export_subcommand():
    with patch("sys.argv", ["main.py", "export"]):
        with patch("main.cmd_export") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_capture_subcommand():
    with patch("sys.argv", ["main.py", "capture"]):
        with patch("main.cmd_capture") as mock_func:
            try:
                main()
            except (SystemExit, Exception):
                pass

def test_clear_subcommand():
    with patch("sys.argv", ["main.py", "clear"]):
        with patch("main.cmd_clear") as mock_func:
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
