"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_check
from config import Config

def test_config(): assert Config is not None

def test_cmd_check():
    args = type('A', (), {'name': 'API Uptime', 'metric': 'uptime', 'target': 99.9, 'value': 99.95, 'unit': '%', 'warning': 0.5, 'json': False})()
    with patch("builtins.print") as p: cmd_check(args)

def test_cmd_check_json():
    args = type('A', (), {'name': 'API Uptime', 'metric': 'uptime', 'target': 99.9, 'value': 99.5, 'unit': '%', 'warning': 0, 'json': True})()
    with patch("builtins.print") as p: cmd_check(args); json.loads(p.call_args[0][0])

def test_main_check():
    with patch("sys.argv", ["main", "check", "Uptime", "--metric", "uptime", "--target", "99.9", "--value", "99.5"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "check", "RT", "--metric", "response_time", "--target", "200", "--value", "150"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
