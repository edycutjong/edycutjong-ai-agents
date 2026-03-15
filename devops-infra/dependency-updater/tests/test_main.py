"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze(tmp_path):
    f = tmp_path / "requirements.txt"; f.write_text("flask==2.0.1\nrequests>=2.28.0\nnumpy")
    args = type('A', (), {'file': str(f)})()
    with patch("builtins.print") as p: cmd_analyze(args); assert len(p.call_args[0][0]) > 0

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-'})()
    with patch("sys.stdin", io.StringIO("flask==2.0.1\nrequests")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze(tmp_path):
    f = tmp_path / "requirements.txt"; f.write_text("django==4.0")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "reqs.txt"; f.write_text("flask")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
