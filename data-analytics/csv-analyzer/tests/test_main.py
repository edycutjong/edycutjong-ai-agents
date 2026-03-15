"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze_file(tmp_path):
    f = tmp_path / "data.csv"
    f.write_text("name,age,score\nAlice,30,95\nBob,25,88\nCharlie,35,92")
    args = type('A', (), {'file': str(f)})()
    with patch("builtins.print") as p: cmd_analyze(args)

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-'})()
    with patch("sys.stdin", io.StringIO("x,y\n1,2\n3,4")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze(tmp_path):
    f = tmp_path / "data.csv"
    f.write_text("a,b\n1,2")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "data.csv"
    f.write_text("a,b\n1,2")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
