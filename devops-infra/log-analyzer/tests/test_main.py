"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze(tmp_path):
    f = tmp_path / "app.log"
    f.write_text("2024-01-01 10:00:00 INFO Application started\n2024-01-01 10:01:00 ERROR Connection failed\n2024-01-01 10:02:00 WARNING Low memory")
    args = type('A', (), {'file': str(f), 'level': None})()
    with patch("builtins.print") as p: cmd_analyze(args)

def test_cmd_analyze_with_level(tmp_path):
    f = tmp_path / "app.log"
    f.write_text("2024-01-01 10:00:00 INFO Started\n2024-01-01 10:01:00 ERROR Crash")
    args = type('A', (), {'file': str(f), 'level': 'ERROR'})()
    with patch("builtins.print") as p: cmd_analyze(args)

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-', 'level': None})()
    with patch("sys.stdin", io.StringIO("2024-01-01 10:00:00 INFO Test")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze(tmp_path):
    f = tmp_path / "app.log"
    f.write_text("2024-01-01 10:00:00 INFO test")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "app.log"
    f.write_text("2024-01-01 10:00:00 INFO test")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
