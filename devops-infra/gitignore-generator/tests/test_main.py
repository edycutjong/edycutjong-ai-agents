"""Tests for gitignore-generator main.py and config.py."""
import os, sys, runpy
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import cmd_generate, cmd_list, main
import config


class TestConfig:
    def test_config_class_exists(self):
        assert hasattr(config, "Config")


class TestCmdGenerate:
    def test_generate_python(self, capsys):
        class Args:
            templates = ["python"]
        cmd_generate(Args())
        out = capsys.readouterr().out
        assert len(out.strip()) > 0


class TestCmdList:
    def test_list_templates(self, capsys):
        class Args:
            pass
        cmd_list(Args())
        out = capsys.readouterr().out
        assert len(out.strip()) > 0


class TestMain:
    @patch("sys.argv", ["main.py", "generate", "python"])
    def test_main_generate(self, capsys):
        main()
        out = capsys.readouterr().out
        assert len(out) > 0

    @patch("sys.argv", ["main.py", "list"])
    def test_main_list(self, capsys):
        main()
        out = capsys.readouterr().out
        assert len(out) > 0

    @patch("sys.argv", ["main.py"])
    def test_main_no_command(self):
        with pytest.raises(SystemExit):
            main()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "list"]):
        runpy.run_path(script, run_name="__main__")
