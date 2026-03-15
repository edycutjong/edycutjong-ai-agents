"""Tests for main.py CLI and config.py."""
import os, sys, io, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate(tmp_path):
    f = tmp_path / "commits.txt"; f.write_text("feat: add login\nfix: resolve crash\nchore: update deps")
    args = type('A', (), {'file': str(f), 'version': '1.0.0', 'json': False})()
    with patch("builtins.print") as p: cmd_generate(args); assert "1.0.0" in p.call_args[0][0]

def test_cmd_generate_json(tmp_path):
    f = tmp_path / "commits.txt"; f.write_text("feat: new feature\nfix: bug fix")
    args = type('A', (), {'file': str(f), 'version': '2.0', 'json': True})()
    with patch("builtins.print") as p: cmd_generate(args); json.loads(p.call_args[0][0])

def test_cmd_generate_stdin():
    args = type('A', (), {'file': '-', 'version': '0.1', 'json': False})()
    with patch("sys.stdin", io.StringIO("feat: something new")):
        with patch("builtins.print") as p: cmd_generate(args)

def test_main_generate(tmp_path):
    f = tmp_path / "c.txt"; f.write_text("feat: init")
    with patch("sys.argv", ["main", "generate", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "c.txt"; f.write_text("fix: fix")
    with patch("sys.argv", ["main", "generate", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
