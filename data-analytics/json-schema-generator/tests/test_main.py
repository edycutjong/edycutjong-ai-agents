"""Tests for main.py CLI and config.py."""
import os, sys, io, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate(tmp_path):
    f = tmp_path / "data.json"
    f.write_text(json.dumps({"name": "Alice", "age": 30, "active": True}))
    args = type('A', (), {'file': str(f), 'title': 'Person'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_generate_stdin():
    args = type('A', (), {'file': '-', 'title': 'Test'})()
    with patch("sys.stdin", io.StringIO('{"x": 1}')):
        with patch("builtins.print") as p: cmd_generate(args)

def test_main_generate(tmp_path):
    f = tmp_path / "data.json"
    f.write_text('{"a": 1}')
    with patch("sys.argv", ["main", "generate", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "data.json"
    f.write_text('{"b": "test"}')
    with patch("sys.argv", ["main", "generate", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
