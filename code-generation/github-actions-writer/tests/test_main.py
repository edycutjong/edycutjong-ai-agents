"""Tests for main.py CLI and config.py."""
import os, sys, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate, cmd_list
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate():
    args = type('A', (), {'template': 'node-ci', 'name': 'CI'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_list():
    with patch("builtins.print") as p: cmd_list(type('A', (), {})())

def test_main_generate():
    with patch("sys.argv", ["main", "generate", "python-ci"]):
        with patch("builtins.print"): main()

def test_main_list():
    with patch("sys.argv", ["main", "list"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "list"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
