"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_explain
from config import Config

def test_config(): assert Config is not None

def test_cmd_explain_file(tmp_path):
    f = tmp_path / "code.py"; f.write_text("def hello(): return 42")
    args = type('A', (), {'file': str(f), 'language': 'python'})()
    with patch("builtins.print") as p: cmd_explain(args); assert len(p.call_args[0][0]) > 0

def test_cmd_explain_stdin():
    args = type('A', (), {'file': '-', 'language': None})()
    with patch("sys.stdin", io.StringIO("x = 1 + 2")):
        with patch("builtins.print") as p: cmd_explain(args); assert len(p.call_args[0][0]) > 0

def test_main_explain(tmp_path):
    f = tmp_path / "code.py"; f.write_text("x = 1")
    with patch("sys.argv", ["main", "explain", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "code.py"; f.write_text("y = 2")
    with patch("sys.argv", ["main", "explain", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
