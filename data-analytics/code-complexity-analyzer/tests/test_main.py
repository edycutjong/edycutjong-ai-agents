"""Tests for code-complexity-analyzer main.py and config.py."""
import os, sys, runpy
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import main
import config
from agent.analyzer import format_result_markdown, calculate_complexity


class TestConfig:
    def test_config_class_exists(self):
        assert hasattr(config, "Config")


class TestMain:
    @patch("sys.argv", ["main.py"])
    def test_main_no_input(self, capsys):
        main()
        out = capsys.readouterr().out
        assert "Code Complexity Analyzer" in out

    @patch("sys.argv", ["main.py", "--help-agent"])
    def test_main_help_agent(self, capsys):
        main()
        out = capsys.readouterr().out
        assert "Usage:" in out

    @patch("sys.argv", ["main.py", "some_code"])
    def test_main_with_input(self, capsys):
        main()
        out = capsys.readouterr().out
        assert "Input: some_code" in out


class TestFormatResultWithIssues:
    def test_format_with_issues(self):
        code = "if True:\n  pass\n" * 30 + "for i in range(10):\n  if i > 5:\n    while True:\n      break\n" * 5
        r = calculate_complexity(code)
        # force issues
        r.issues.append("Test issue")
        md = format_result_markdown(r)
        assert "⚠️" in md


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "--help-agent"]):
        runpy.run_path(script, run_name="__main__")
