"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate_markdown():
    args = type('A', (), {'topic': 'Python', 'count': 2, 'json': False})()
    with patch("builtins.print") as p: cmd_generate(args); assert len(p.call_args[0][0]) > 0

def test_cmd_generate_json():
    args = type('A', (), {'topic': 'Git', 'count': 2, 'json': True})()
    with patch("builtins.print") as p: cmd_generate(args); json.loads(p.call_args[0][0])

def test_main_generate():
    with patch("sys.argv", ["main", "generate", "Docker"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "generate", "SQL"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
