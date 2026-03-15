import os
import sys
import runpy
from io import StringIO
from unittest.mock import patch
import pytest

# Ensure we have the parent directory in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import cmd_analyze, cmd_optimize, cmd_compare, main
import config

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_config():
    assert hasattr(config, "Config")

def test_cmd_analyze_string(capsys):
    args = DummyArgs(prompt="Tell me a joke", json=False)
    cmd_analyze(args)
    captured = capsys.readouterr()
    assert "Prompt Analysis" in captured.out

def test_cmd_analyze_stdin(capsys):
    args = DummyArgs(prompt="-", json=False)
    with patch("sys.stdin", StringIO("Explain quantum physics")):
        cmd_analyze(args)
    captured = capsys.readouterr()
    assert "Prompt Analysis" in captured.out

def test_cmd_analyze_json(capsys):
    args = DummyArgs(prompt="Tell me a joke format as JSON", json=True)
    cmd_analyze(args)
    captured = capsys.readouterr()
    assert '"score"' in captured.out

def test_cmd_optimize_string(capsys):
    args = DummyArgs(prompt="Write a poem")
    cmd_optimize(args)
    captured = capsys.readouterr()
    assert "Write a poem" in captured.out

def test_cmd_optimize_stdin(capsys):
    args = DummyArgs(prompt="-")
    with patch("sys.stdin", StringIO("Write a story")):
        cmd_optimize(args)
    captured = capsys.readouterr()
    assert "Write a story" in captured.out

def test_cmd_compare(capsys):
    args = DummyArgs(prompt_a="Write a poem", prompt_b="Write a poem format as JSON")
    cmd_compare(args)
    captured = capsys.readouterr()
    assert "Winner:" in captured.out

@patch("sys.argv", ["main.py", "analyze", "Tell me a joke"])
def test_main_analyze(capsys):
    with patch("main.cmd_analyze") as mock_analyze:
        main()
        mock_analyze.assert_called_once()

@patch("sys.argv", ["main.py", "optimize", "Tell me a joke"])
def test_main_optimize(capsys):
    with patch("main.cmd_optimize") as mock_optimize:
        main()
        mock_optimize.assert_called_once()

@patch("sys.argv", ["main.py", "compare", "A", "B"])
def test_main_compare(capsys):
    with patch("main.cmd_compare") as mock_compare:
        main()
        mock_compare.assert_called_once()

def test_main_block():
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "analyze", "Tell me a joke"]):
        runpy.run_path(script_path, run_name="__main__")
