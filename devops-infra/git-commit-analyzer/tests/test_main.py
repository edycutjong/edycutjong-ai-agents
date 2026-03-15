"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze(tmp_path):
    f = tmp_path / "commits.txt"
    f.write_text("abc1234 feat: add login\ndef5678 fix: resolve crash\nghi9012 chore: update deps")
    args = type('A', (), {'file': str(f)})()
    with patch("builtins.print") as p: cmd_analyze(args)

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-'})()
    with patch("sys.stdin", io.StringIO("abc1234 feat: add search")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze(tmp_path):
    f = tmp_path / "c.txt"
    f.write_text("abc feat: init")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "c.txt"
    f.write_text("abc fix: bug")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
