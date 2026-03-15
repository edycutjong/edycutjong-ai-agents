"""Tests for main.py CLI."""
import json, os, sys, pytest, tempfile
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main, cmd_add, cmd_list, cmd_update
from agent.tracker import OKRStore


class TestCLI:
    def test_cmd_add(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            with open(store_file, "w") as f:
                json.dump([], f)
            args = type('Args', (), {
                'title': 'Ship v2', 'owner': 'Alice', 'quarter': 'Q1',
                'key_results': ['Feature A', 'Feature B'], 'target': 100
            })()
            with patch("builtins.print") as mock_print:
                cmd_add(args)
                assert "Added" in mock_print.call_args[0][0]

    def test_cmd_list_markdown(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with open(store_file, "w") as f:
            json.dump([{"id": "abc", "title": "Goal", "status": "on-track", "progress": 50, "key_results": []}], f)
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            args = type('Args', (), {'json': False})()
            with patch("builtins.print") as mock_print:
                cmd_list(args)
                assert "OKR Dashboard" in mock_print.call_args[0][0]

    def test_cmd_list_json(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with open(store_file, "w") as f:
            json.dump([{"id": "abc", "title": "Goal", "status": "behind", "progress": 10, "key_results": []}], f)
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            args = type('Args', (), {'json': True})()
            with patch("builtins.print") as mock_print:
                cmd_list(args)
                parsed = json.loads(mock_print.call_args[0][0])
                assert parsed[0]["id"] == "abc"

    def test_cmd_update(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with open(store_file, "w") as f:
            json.dump([{"id": "o1", "title": "G", "key_results": [{"id": "kr1", "title": "KR", "target": 100, "current": 0}]}], f)
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            args = type('Args', (), {'objective_id': 'o1', 'kr_id': 'kr1', 'value': 75})()
            with patch("builtins.print") as mock_print:
                cmd_update(args)
                assert "Updated" in mock_print.call_args[0][0]

    def test_cmd_update_not_found(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with open(store_file, "w") as f:
            json.dump([], f)
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            args = type('Args', (), {'objective_id': 'xxx', 'kr_id': 'yyy', 'value': 50})()
            with patch("builtins.print") as mock_print:
                cmd_update(args)
                assert "Not found" in mock_print.call_args[0][0]

    def test_main_add(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with open(store_file, "w") as f:
            json.dump([], f)
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            with patch("sys.argv", ["main", "add", "My Goal", "--owner", "Bob"]):
                with patch("builtins.print"):
                    main()

    def test_main_entry_point(self, tmp_path):
        store_file = tmp_path / "okrs.json"
        with open(store_file, "w") as f:
            json.dump([], f)
        with patch.object(OKRStore, '__init__', lambda self, *a, **kw: setattr(self, 'filepath', str(store_file)) or None):
            with patch("sys.argv", ["main", "list"]):
                with patch("builtins.print"):
                    with patch.dict('sys.modules', {'__main__': None}):
                        runpy.run_module('main', run_name='__main__', alter_sys=True)
