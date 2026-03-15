"""Tests for main.py CLI and config.py."""
import os, sys, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate_express():
    args = type('A', (), {'model': 'User: name:string, email:string', 'framework': 'express'})()
    with patch("builtins.print") as p: cmd_generate(args); assert "router" in p.call_args[0][0].lower() or "app" in p.call_args[0][0].lower()

def test_cmd_generate_fastapi():
    args = type('A', (), {'model': 'User: name:string', 'framework': 'fastapi'})()
    with patch("builtins.print") as p: cmd_generate(args); assert "User" in p.call_args[0][0] or "app" in p.call_args[0][0].lower()

def test_main_generate():
    with patch("sys.argv", ["main", "generate", "Post: title:string"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "generate", "Item: name:string"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
