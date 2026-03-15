"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze():
    args = type('A', (), {'query': 'SELECT * FROM users'})()
    with patch("builtins.print") as p: cmd_analyze(args); assert len(p.call_args[0][0]) > 0

def test_cmd_analyze_stdin():
    args = type('A', (), {'query': '-'})()
    with patch("sys.stdin", io.StringIO("SELECT id FROM orders WHERE status = 'active'")):
        with patch("builtins.print") as p: cmd_analyze(args); assert len(p.call_args[0][0]) > 0

def test_main_analyze():
    with patch("sys.argv", ["main", "analyze", "SELECT * FROM users"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "analyze", "SELECT 1"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
