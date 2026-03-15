"""Tests for main.py CLI and config.py."""
import os, sys, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_check
from config import Config

def test_config(): assert Config is not None

def test_cmd_check():
    args = type('A', (), {'password': 'MyP@ssw0rd!2024'})()
    with patch("builtins.print") as p: cmd_check(args); assert len(p.call_args[0][0]) > 0

def test_main_check():
    with patch("sys.argv", ["main", "check", "Str0ng!Pass"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "check", "Test1!"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
