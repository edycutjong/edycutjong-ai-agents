"""Tests for main.py CLI and config.py."""
import os, sys, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate():
    args = type('A', (), {'schema': 'user', 'count': 3, 'csv': False})()
    with patch("builtins.print") as p: cmd_generate(args); assert len(p.call_args[0][0]) > 0

def test_cmd_generate_csv():
    args = type('A', (), {'schema': 'product', 'count': 2, 'csv': True})()
    with patch("builtins.print") as p: cmd_generate(args); assert len(p.call_args[0][0]) > 0

def test_main_generate():
    with patch("sys.argv", ["main", "generate", "order", "--count", "2"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "generate", "user"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
