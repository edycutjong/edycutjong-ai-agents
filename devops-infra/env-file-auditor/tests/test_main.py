"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_audit, cmd_compare, cmd_template
from config import Config

def test_config(): assert Config is not None

def test_cmd_audit(tmp_path):
    f = tmp_path / ".env"
    f.write_text("DB_HOST=localhost\nAPI_KEY=secret123\nDEBUG=true")
    args = type('A', (), {'file': str(f), 'json': False})()
    with patch("builtins.print") as p: cmd_audit(args)

def test_cmd_audit_json(tmp_path):
    f = tmp_path / ".env"
    f.write_text("PORT=3000")
    args = type('A', (), {'file': str(f), 'json': True})()
    with patch("builtins.print") as p: cmd_audit(args)

def test_cmd_compare(tmp_path):
    a = tmp_path / ".env.a"; a.write_text("KEY=val1\nDB=local")
    b = tmp_path / ".env.b"; b.write_text("KEY=val2\nREDIS=yes")
    args = type('A', (), {'file_a': str(a), 'file_b': str(b)})()
    with patch("builtins.print") as p: cmd_compare(args)

def test_cmd_template(tmp_path):
    f = tmp_path / ".env"
    f.write_text("SECRET_KEY=abc\nPORT=3000")
    args = type('A', (), {'file': str(f)})()
    with patch("builtins.print") as p: cmd_template(args)

def test_main_audit(tmp_path):
    f = tmp_path / ".env"; f.write_text("X=1")
    with patch("sys.argv", ["main", "audit", str(f)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    f = tmp_path / ".env"; f.write_text("X=1")
    with patch("sys.argv", ["main", "audit", str(f)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
