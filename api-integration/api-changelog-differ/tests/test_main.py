"""Tests for main.py CLI and config.py."""
import os, sys, json, pytest
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, cmd_diff
from config import Config

def test_config(): assert Config is not None

def test_cmd_diff(tmp_path):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps({"info": {"version": "1.0"}, "paths": {"/api/users": {"get": {"responses": {"200": {}}}}}, "components": {"schemas": {"User": {"properties": {"id": {}}, "required": ["id"]}}}}))
    new.write_text(json.dumps({"info": {"version": "2.0"}, "paths": {"/api/users": {"get": {"responses": {"200": {}}}}, "/api/posts": {"get": {}}}, "components": {"schemas": {"User": {"properties": {"id": {}, "email": {}}, "required": ["id", "email"]}}}}))
    args = type('A', (), {'old': str(old), 'new': str(new), 'json': False, 'fail_on_breaking': False})()
    with patch("builtins.print") as p: cmd_diff(args)

def test_cmd_diff_json(tmp_path):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps({"info": {"version": "1.0"}, "paths": {}, "components": {"schemas": {}}}))
    new.write_text(json.dumps({"info": {"version": "1.1"}, "paths": {}, "components": {"schemas": {}}}))
    args = type('A', (), {'old': str(old), 'new': str(new), 'json': True, 'fail_on_breaking': False})()
    with patch("builtins.print") as p: cmd_diff(args); json.loads(p.call_args[0][0])

def test_cmd_diff_fail_on_breaking(tmp_path):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps({"info": {"version": "1.0"}, "paths": {"/api/users": {"get": {}}}, "components": {"schemas": {}}}))
    new.write_text(json.dumps({"info": {"version": "2.0"}, "paths": {}, "components": {"schemas": {}}}))
    args = type('A', (), {'old': str(old), 'new': str(new), 'json': False, 'fail_on_breaking': True})()
    with patch("builtins.print"):
        with pytest.raises(SystemExit): cmd_diff(args)

def test_main_diff(tmp_path):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps({"info": {"version": "1"}, "paths": {}, "components": {"schemas": {}}}))
    new.write_text(json.dumps({"info": {"version": "2"}, "paths": {}, "components": {"schemas": {}}}))
    with patch("sys.argv", ["main", "diff", str(old), str(new)]):
        with patch("builtins.print"): main()

def test_main_entry_point(tmp_path):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps({"info": {"version": "1"}, "paths": {}, "components": {"schemas": {}}}))
    new.write_text(json.dumps({"info": {"version": "2"}, "paths": {}, "components": {"schemas": {}}}))
    with patch("sys.argv", ["main", "diff", str(old), str(new)]):
        with patch("builtins.print"):
            with patch.dict("sys.modules", {"__main__": None}):
                runpy.run_module("main", run_name="__main__", alter_sys=True)
