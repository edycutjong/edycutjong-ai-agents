"""Tests for main.py CLI and config.py."""
import os, sys, io, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze():
    args = type('A', (), {'subject': 'Urgent: Verify your account', 'body': 'Click here to verify your account at somebank.evil.com', 'sender': 'notsafe@evil.com', 'json': False})()
    with patch("builtins.print") as p: cmd_analyze(args); assert len(p.call_args[0][0]) > 0

def test_cmd_analyze_json():
    args = type('A', (), {'subject': 'Hello', 'body': 'Normal email', 'sender': 'friend@legit.com', 'json': True})()
    with patch("builtins.print") as p: cmd_analyze(args); json.loads(p.call_args[0][0])

def test_cmd_analyze_stdin():
    args = type('A', (), {'subject': 'Test', 'body': '-', 'sender': '', 'json': False})()
    with patch("sys.stdin", io.StringIO("This is the email body content")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze():
    with patch("sys.argv", ["main", "analyze", "--subject", "Test", "--body", "Hello"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "analyze", "--subject", "Hey", "--body", "World"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
