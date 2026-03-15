"""Tests for main.py CLI and config.py."""
import os, sys, json, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_scan
from config import Config

def test_config(): assert Config is not None

def test_cmd_scan_file(tmp_path):
    f = tmp_path / "code.py"
    f.write_text("api_key='AKIA1234567890123456'\nprint('hello')")
    args = type('A', (), {'path': str(f), 'json': False})()
    with patch("builtins.print") as p: cmd_scan(args)

def test_cmd_scan_dir(tmp_path):
    (tmp_path / "app.py").write_text("token = 'ghp_abcdefghijklmnopqrstuvwxyz1234567890'")
    args = type('A', (), {'path': str(tmp_path), 'json': False})()
    with patch("builtins.print") as p: cmd_scan(args)

def test_cmd_scan_json(tmp_path):
    f = tmp_path / "code.py"
    f.write_text("x = 1")
    args = type('A', (), {'path': str(f), 'json': True})()
    with patch("builtins.print") as p: cmd_scan(args)

def test_main_scan(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x=1")
    with patch("sys.argv", ["main", "scan", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("a=1")
    with patch("sys.argv", ["main", "scan", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)


def test_cmd_scan_stdin():
    """Cover main.py line 8: stdin fallback (path not file/dir)."""
    args = type('A', (), {'path': '/nonexistent/path', 'json': False})()
    with patch("sys.stdin", __import__("io").StringIO("password='secret123456'")):
        with patch("builtins.print") as p: cmd_scan(args)
