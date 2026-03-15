import pytest
from unittest.mock import patch, mock_open
import sys
import runpy

from main import cmd_generate, main
from config import Config

def test_config():
    assert Config is not None

def test_cmd_generate_stdin(capsys):
    class Args:
        file = "-"
        version = "Unreleased"
    with patch("sys.stdin.read", return_value="feat: added something\nfix: fixed a bug"):
        cmd_generate(Args())
    captured = capsys.readouterr()
    assert "Unreleased" in captured.out
    assert "added something" in captured.out
    assert "fixed a bug" in captured.out

def test_cmd_generate_file(capsys):
    class Args:
        file = "logs.txt"
        version = "v1.0.0"
    with patch("builtins.open", mock_open(read_data="feat: awesome feature\nchore: clean up")):
        cmd_generate(Args())
    captured = capsys.readouterr()
    assert "v1.0.0" in captured.out
    assert "awesome feature" in captured.out
    assert "clean up" in captured.out

def test_main():
    with patch("sys.argv", ["main.py", "generate", "-", "--version", "v2.0.0"]), \
         patch("sys.stdin.read", return_value="feat: main function\n"):
        main()

def test_main_block():
    with patch("sys.argv", ["main.py", "generate", "-"]), \
         patch("sys.stdin.read", return_value="feat: main test\n"):
        runpy.run_module("main", run_name="__main__")
