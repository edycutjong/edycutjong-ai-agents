"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate, cmd_validate, cmd_templates
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate():
    args = type('A', (), {'category': 'qa', 'count': 2, 'vars': ['topic=AI', 'definition=artificial intelligence'], 'format': 'alpaca'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_generate_chat():
    args = type('A', (), {'category': 'qa', 'count': 1, 'vars': ['topic=ML', 'definition=machine learning'], 'format': 'chat'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_generate_completion():
    args = type('A', (), {'category': 'qa', 'count': 1, 'vars': ['topic=AI', 'definition=test'], 'format': 'completion'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_generate_jsonl():
    args = type('A', (), {'category': 'qa', 'count': 1, 'vars': ['topic=X', 'definition=Y'], 'format': 'jsonl'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_validate(tmp_path):
    f = tmp_path / "data.json"
    f.write_text(json.dumps([{"instruction": "Test question here.", "input": "", "output": "Answer", "category": "qa", "quality": 1.0}]))
    args = type('A', (), {'file': str(f)})()
    with patch("builtins.print") as p: cmd_validate(args)

def test_cmd_templates():
    with patch("builtins.print") as p: cmd_templates(type('A', (), {})())

def test_main_generate():
    with patch("sys.argv", ["main", "generate", "--category", "qa", "--count", "1", "--vars", "topic=test", "definition=def"]):
        with patch("builtins.print"): main()

def test_main_entry_point():
    with patch("sys.argv", ["main", "templates"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
