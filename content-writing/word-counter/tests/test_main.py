import pytest
from unittest.mock import patch, mock_open
import sys
import runpy

from main import cmd_count, main
from config import Config

def test_config():
    assert Config is not None

def test_cmd_count_stdin(capsys):
    class Args:
        file = "-"
    
    with patch("sys.stdin.read", return_value="hello world"):
        cmd_count(Args())
    
    captured = capsys.readouterr()
    assert "Word Count" in captured.out
    assert "2" in captured.out

def test_cmd_count_file(capsys):
    class Args:
        file = "dummy.txt"
    
    with patch("builtins.open", mock_open(read_data="hello file world")):
        cmd_count(Args())
        
    captured = capsys.readouterr()
    assert "Word Count" in captured.out
    assert "3" in captured.out

def test_main():
    with patch("sys.argv", ["main.py", "count", "-"]), \
         patch("sys.stdin.read", return_value="test text"):
        main()

def test_main_block():
    with patch("sys.argv", ["main.py", "count", "-"]), \
         patch("sys.stdin.read", return_value="test text"):
        runpy.run_module("main", run_name="__main__")
