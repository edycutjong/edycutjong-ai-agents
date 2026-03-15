"""Tests for main.py CLI and config.py."""
import json, os, sys, pytest, io
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_analyze
from config import Config
from agent.analyzer import parse_schema

def test_config(): assert Config is not None

def test_cmd_analyze_markdown(tmp_path):
    sdl = "type Query { hello: String }\ntype User { id: ID! name: String }"
    f = tmp_path / "schema.graphql"; f.write_text(sdl)
    args = type('A', (), {'file': str(f), 'json': False})()
    with patch("builtins.print") as p: cmd_analyze(args); assert "Query" in p.call_args[0][0]

def test_cmd_analyze_json(tmp_path):
    sdl = "type Query { hello: String }"
    f = tmp_path / "schema.graphql"; f.write_text(sdl)
    args = type('A', (), {'file': str(f), 'json': True})()
    with patch("builtins.print") as p: cmd_analyze(args); json.loads(p.call_args[0][0])

def test_cmd_analyze_stdin():
    args = type('A', (), {'file': '-', 'json': False})()
    with patch("sys.stdin", io.StringIO("type Query { hello: String }")):
        with patch("builtins.print") as p: cmd_analyze(args); assert "Query" in p.call_args[0][0]

def test_main_analyze(tmp_path):
    f = tmp_path / "s.graphql"; f.write_text("type Query { x: String }")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "s.graphql"; f.write_text("type Query { x: String }")
    with patch("sys.argv", ["main", "analyze", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
