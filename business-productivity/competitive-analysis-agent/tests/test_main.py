"""Tests for main.py CLI and config.py."""
import json, os, sys, pytest, tempfile
from unittest.mock import patch
import runpy

# Ensure parent dir is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main, cmd_analyze
from config import Config
from agent.analyzer import Competitor


class TestConfig:
    def test_config_class_exists(self):
        assert Config is not None


class TestCLI:
    def test_cmd_analyze_markdown(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "your_product": {"name": "MyApp", "features": ["auth"], "strengths": ["fast"]},
            "competitors": [{"name": "Rival", "features": ["auth", "billing"]}]
        }))
        args = type('Args', (), {'config': str(config_file), 'json': False})()
        with patch("builtins.print") as mock_print:
            cmd_analyze(args)
            output = mock_print.call_args[0][0]
            assert "MyApp" in output

    def test_cmd_analyze_json(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "your_product": {"name": "MyApp", "features": ["auth"]},
            "competitors": [{"name": "Rival", "features": ["auth"]}]
        }))
        args = type('Args', (), {'config': str(config_file), 'json': True})()
        with patch("builtins.print") as mock_print:
            cmd_analyze(args)
            output = mock_print.call_args[0][0]
            parsed = json.loads(output)
            assert parsed["your_product"]["name"] == "MyApp"

    def test_main_analyze(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "your_product": {"name": "Test", "features": ["x"]},
            "competitors": []
        }))
        with patch("sys.argv", ["main", "analyze", str(config_file)]):
            with patch("builtins.print"):
                main()

    def test_main_entry_point(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "your_product": {"name": "Test", "features": []},
            "competitors": []
        }))
        with patch("sys.argv", ["main", "analyze", str(config_file)]):
            with patch("builtins.print"):
                with patch.dict('sys.modules', {'__main__': None}):
                    runpy.run_module('main', run_name='__main__', alter_sys=True)
