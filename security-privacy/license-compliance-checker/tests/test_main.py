"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_check
from config import Config

def test_config(): assert Config is not None

def test_cmd_check_requirements(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("flask==2.0.0\nrequests>=2.28")
    args = type('A', (), {'file': str(f), 'license': 'MIT'})()
    with patch("builtins.print") as p: cmd_check(args)

def test_cmd_check_package_json(tmp_path):
    f = tmp_path / "package.json"
    f.write_text(json.dumps({"dependencies": {"react": "^18"}, "devDependencies": {"jest": "^29"}}))
    args = type('A', (), {'file': str(f), 'license': 'MIT'})()
    with patch("builtins.print") as p: cmd_check(args)

def test_main_check(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("django==4.0")
    with patch("sys.argv", ["main", "check", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("flask==2.0")
    with patch("sys.argv", ["main", "check", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
