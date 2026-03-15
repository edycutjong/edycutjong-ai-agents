"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_dedupe
from config import Config

def test_config(): assert Config is not None

def test_cmd_dedupe(tmp_path):
    f = tmp_path / "data.csv"; f.write_text("name,email\nAlice,a@b.com\nBob,b@c.com\nAlice,a@b.com")
    args = type('A', (), {'file': str(f), 'report': False})()
    with patch("builtins.print") as p: cmd_dedupe(args)

def test_cmd_dedupe_report(tmp_path):
    f = tmp_path / "data.csv"; f.write_text("name,email\nAlice,a@b.com\nAlice,a@b.com\nBob,b@c.com")
    args = type('A', (), {'file': str(f), 'report': True})()
    with patch("builtins.print") as p: cmd_dedupe(args)

def test_cmd_dedupe_stdin():
    args = type('A', (), {'file': '-', 'report': False})()
    with patch("sys.stdin", io.StringIO("a,b\n1,2\n1,2\n3,4")):
        with patch("builtins.print") as p: cmd_dedupe(args)

def test_main_dedupe(tmp_path):
    f = tmp_path / "data.csv"; f.write_text("a\n1\n1")
    with patch("sys.argv", ["main", "dedupe", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "data.csv"; f.write_text("x\n1\n1")
    with patch("sys.argv", ["main", "dedupe", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
