"""Tests for main.py CLI and config.py."""
import os, sys, json, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze(tmp_path):
    f = tmp_path / "ts.csv"
    f.write_text("date,project,hours,description\n2024-01-01,Alpha,8.0,coding\n2024-01-02,Beta,6.5,review")
    args = type('A', (), {'file': str(f), 'target': 8.0, 'json': False})()
    with patch("builtins.print") as p: cmd_analyze(args)

def test_cmd_analyze_json(tmp_path):
    f = tmp_path / "ts.csv"
    f.write_text("date,project,hours\n2024-01-01,Alpha,7.0")
    args = type('A', (), {'file': str(f), 'target': 8.0, 'json': True})()
    with patch("builtins.print") as p: cmd_analyze(args); json.loads(p.call_args[0][0])

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-', 'target': 8.0, 'json': False})()
    with patch("sys.stdin", io.StringIO("date,project,hours\n2024-01-01,X,5.0")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze(tmp_path):
    f = tmp_path / "ts.csv"
    f.write_text("date,project,hours\n2024-01-01,A,8.0")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "ts.csv"
    f.write_text("date,project,hours\n2024-01-01,A,8.0")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
