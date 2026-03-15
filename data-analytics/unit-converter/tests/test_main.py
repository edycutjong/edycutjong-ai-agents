"""Tests for unit-converter main.py and config.py."""
import os, sys, runpy
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import cmd_convert, main
import config


class TestConfig:
    def test_config_class_exists(self):
        assert hasattr(config, "Config")


class TestCmdConvert:
    def test_convert_length(self, capsys):
        class Args:
            value = 1.0; from_unit = "km"; to_unit = "m"
        cmd_convert(Args())
        out = capsys.readouterr().out
        assert "1000" in out

    def test_convert_invalid(self, capsys):
        class Args:
            value = 1.0; from_unit = "xyz"; to_unit = "m"
        cmd_convert(Args())
        out = capsys.readouterr().out
        assert "Error" in out or "Unknown" in out


class TestMain:
    @patch("sys.argv", ["main.py", "convert", "100", "cm", "m"])
    def test_main_convert(self, capsys):
        main()
        out = capsys.readouterr().out
        assert "1" in out

    @patch("sys.argv", ["main.py"])
    def test_main_no_command(self):
        with pytest.raises(SystemExit):
            main()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "convert", "5", "km", "m"]):
        runpy.run_path(script, run_name="__main__")
