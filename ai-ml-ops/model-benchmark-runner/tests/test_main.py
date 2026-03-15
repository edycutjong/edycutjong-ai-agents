"""Tests for main.py CLI."""
import os, sys, json, pytest
from unittest.mock import patch, MagicMock
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_run, cmd_history

def test_cmd_run(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({
        "cases": [{"prompt": "What is 1+1?", "expected": "2", "category": "math"}],
        "model_outputs": {"test-model": ["2"]}
    }))
    args = type('A', (), {'config': str(cfg), 'json': False, 'save': False})()
    with patch("builtins.print") as p: cmd_run(args)

def test_cmd_run_json(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({
        "cases": [{"prompt": "Hello", "expected": "Hi"}],
        "model_outputs": {"model-a": ["Hi"]}
    }))
    args = type('A', (), {'config': str(cfg), 'json': True, 'save': False})()
    with patch("builtins.print") as p: cmd_run(args); json.loads(p.call_args[0][0])

def test_cmd_run_save(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({
        "cases": [{"prompt": "q", "expected": "a"}],
        "model_outputs": {"model-x": ["a"]}
    }))
    args = type('A', (), {'config': str(cfg), 'json': False, 'save': True})()
    with patch("builtins.print"), patch("main.BenchmarkStorage") as MockStorage:
        MockStorage.return_value.save = MagicMock()
        cmd_run(args)

def test_cmd_history():
    with patch("main.BenchmarkStorage") as MockStorage:
        MockStorage.return_value.get_all.return_value = [
            {"timestamp": "2024-01-01", "models": ["gpt-4"], "summary": {"winner": "gpt-4"}}
        ]
        with patch("builtins.print") as p: cmd_history(type('A', (), {})())

def test_main_run(tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"cases": [{"prompt": "x", "expected": "y"}], "model_outputs": {"m": ["y"]}}))
    with patch("sys.argv", ["main", "run", str(cfg)]):
        with patch("builtins.print"): main()

def test_main_history():
    with patch("sys.argv", ["main", "history"]):
        with patch("main.BenchmarkStorage") as MockStorage:
            MockStorage.return_value.get_all.return_value = []
            main()

def test_main_entry_point(tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"cases": [{"prompt": "x", "expected": "y"}], "model_outputs": {"m": ["y"]}}))
    with patch("sys.argv", ["main", "run", str(cfg)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
