"""Tests for main.py CLI and config.py."""
import os, sys, json, io, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config

def test_config(): assert Config is not None

def test_cmd_analyze(tmp_path):
    f = tmp_path / "Dockerfile"; f.write_text("FROM python:3.11\nRUN pip install flask\nCOPY . /app\nWORKDIR /app\nCMD [\"python\", \"app.py\"]")
    args = type('A', (), {'file': str(f), 'json': False})()
    with patch("builtins.print") as p: cmd_analyze(args); assert len(p.call_args[0][0]) > 0

def test_cmd_analyze_json(tmp_path):
    f = tmp_path / "Dockerfile"; f.write_text("FROM node:18\nCOPY . .\nRUN npm install")
    args = type('A', (), {'file': str(f), 'json': True})()
    with patch("builtins.print") as p: cmd_analyze(args); json.loads(p.call_args[0][0])

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-', 'json': False})()
    with patch("sys.stdin", io.StringIO("FROM python:3.9\nRUN pip install requests")):
        with patch("builtins.print") as p: cmd_analyze(args)

def test_main_analyze(tmp_path):
    f = tmp_path / "Dockerfile"; f.write_text("FROM python:3.9\nRUN pip install requests")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "Dockerfile"; f.write_text("FROM python:3.9\nRUN pip install requests")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
