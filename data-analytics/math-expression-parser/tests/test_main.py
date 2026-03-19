import os
import sys
import runpy
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import main

def test_main_help_agent(capsys):
    with patch("sys.argv", ["main.py", "--help-agent"]):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out

def test_main_no_args(capsys):
    with patch("sys.argv", ["main.py"]):
        main()
    captured = capsys.readouterr()
    assert "Usage:" in captured.out

def test_main_with_input(capsys):
    with patch("sys.argv", ["main.py", "test_input"]):
        main()
    captured = capsys.readouterr()
    assert "Input: test_input" in captured.out

def test_main_with_file(capsys, tmp_path):
    p = tmp_path / "test_input.txt"
    p.write_text("test string data here")
    with patch("sys.argv", ["main.py", str(p)]):
        main()
    captured = capsys.readouterr()

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "--help-agent"]):
        runpy.run_path(script_path, run_name="__main__")
