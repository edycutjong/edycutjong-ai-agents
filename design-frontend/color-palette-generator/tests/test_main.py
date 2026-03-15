"""Tests for main.py CLI and config.py."""
import os, sys, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate():
    args = type('A', (), {'color': '#FF5733', 'scheme': 'complementary'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_generate_analogous():
    args = type('A', (), {'color': '#3498DB', 'scheme': 'analogous'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_main_generate():
    with patch("sys.argv", ["main", "generate", "#00FF00"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "generate", "#ABCDEF"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
