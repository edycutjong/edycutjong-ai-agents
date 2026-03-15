"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_generate
from config import Config

def test_config(): assert Config is not None

def test_cmd_generate_markdown(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("from flask import Flask\napp = Flask(__name__)\n@app.route('/users', methods=['GET'])\ndef get_users():\n    \"\"\"Get all users.\"\"\"\n    return []")
    args = type('A', (), {'file': str(f), 'framework': None, 'format': 'markdown', 'title': 'Test API'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_cmd_generate_openapi(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("from flask import Flask\napp = Flask(__name__)\n@app.route('/users', methods=['GET'])\ndef get_users():\n    return []")
    args = type('A', (), {'file': str(f), 'framework': 'flask', 'format': 'openapi', 'title': 'API'})()
    with patch("builtins.print") as p: cmd_generate(args)

def test_main_generate(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("app.get('/test', (req, res) => {})")
    with patch("sys.argv", ["main", "generate", str(f), "--framework", "express"]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "app.py"
    f.write_text("@app.get('/items')\ndef items(): pass")
    with patch("sys.argv", ["main", "generate", str(f), "--framework", "fastapi"]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
