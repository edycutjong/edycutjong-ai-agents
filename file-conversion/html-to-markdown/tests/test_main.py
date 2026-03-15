"""Tests for main.py CLI and config.py."""
import os, sys, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_convert
from config import Config

def test_config(): assert Config is not None

def test_cmd_convert_file(tmp_path):
    f = tmp_path / "page.html"
    f.write_text("<h1>Hello</h1><p>World</p>")
    args = type('A', (), {'file': str(f)})()
    with patch("builtins.print") as p: cmd_convert(args)

def test_cmd_convert_stdin():
    args = type('A', (), {'file': '-'})()
    with patch("sys.stdin", io.StringIO("<h2>Test</h2>")):
        with patch("builtins.print") as p: cmd_convert(args)

def test_main_convert(tmp_path):
    f = tmp_path / "page.html"
    f.write_text("<h1>Hi</h1>")
    with patch("sys.argv", ["main", "convert", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "page.html"
    f.write_text("<b>Bold</b>")
    with patch("sys.argv", ["main", "convert", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
