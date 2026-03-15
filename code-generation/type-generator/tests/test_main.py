"""Tests for main.py CLI and config.py."""
import json, os, sys, pytest, io
from unittest.mock import patch
import runpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main, cmd_generate
from config import Config


class TestConfig:
    def test_config_class_exists(self):
        assert Config is not None


class TestCLI:
    def test_cmd_generate_typescript_from_file(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps({"name": "Alice", "age": 30}))
        args = type('Args', (), {'file': str(data_file), 'name': 'User', 'format': 'typescript'})()
        with patch("builtins.print") as mock_print:
            cmd_generate(args)
            output = mock_print.call_args[0][0]
            assert "interface User" in output

    def test_cmd_generate_from_stdin(self):
        args = type('Args', (), {'file': '-', 'name': 'Root', 'format': 'typescript'})()
        with patch("sys.stdin", io.StringIO('{"key": "value"}')):
            with patch("builtins.print") as mock_print:
                cmd_generate(args)
                assert "interface Root" in mock_print.call_args[0][0]

    def test_cmd_generate_python(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps({"x": 1}))
        args = type('Args', (), {'file': str(data_file), 'name': 'MyType', 'format': 'python'})()
        with patch("builtins.print") as mock_print:
            cmd_generate(args)
            assert "class MyType" in mock_print.call_args[0][0]

    def test_cmd_generate_zod(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps({"x": 1}))
        args = type('Args', (), {'file': str(data_file), 'name': 'Schema', 'format': 'zod'})()
        with patch("builtins.print") as mock_print:
            cmd_generate(args)
            assert "SchemaSchema" in mock_print.call_args[0][0]

    def test_main_generate(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps({"a": 1}))
        with patch("sys.argv", ["main", "generate", str(data_file)]):
            with patch("builtins.print"):
                main()

    def test_main_entry_point(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps({"b": "c"}))
        with patch("sys.argv", ["main", "generate", str(data_file)]):
            with patch("builtins.print"):
                with patch.dict('sys.modules', {'__main__': None}):
                    runpy.run_module('main', run_name='__main__', alter_sys=True)
