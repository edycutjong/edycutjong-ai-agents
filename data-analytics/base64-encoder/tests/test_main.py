"""Tests for base64-encoder main.py and config.py."""
import os, sys, runpy
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import cmd_encode, cmd_decode, cmd_auto, main
import config


class TestConfig:
    def test_config_class_exists(self):
        assert hasattr(config, "Config")


class TestCmdEncode:
    def test_encode_text(self, capsys):
        class Args:
            text = "hello"; url_safe = False
        cmd_encode(Args())
        out = capsys.readouterr().out
        assert "Base64" in out

    def test_encode_url_safe(self, capsys):
        class Args:
            text = "hello world"; url_safe = True
        cmd_encode(Args())
        out = capsys.readouterr().out
        assert len(out) > 0


class TestCmdDecode:
    def test_decode_text(self, capsys):
        class Args:
            text = "aGVsbG8="; url_safe = False
        cmd_decode(Args())
        out = capsys.readouterr().out
        assert "Base64" in out

    def test_decode_url_safe(self, capsys):
        class Args:
            text = "aGVsbG8="; url_safe = True
        cmd_decode(Args())
        out = capsys.readouterr().out
        assert len(out) > 0


class TestCmdAuto:
    def test_auto_detect_valid_base64(self, capsys):
        class Args:
            text = "aGVsbG8="
        cmd_auto(Args())
        out = capsys.readouterr().out
        assert "Base64" in out

    def test_auto_detect_plain_text(self, capsys):
        class Args:
            text = "hello world!!!"
        cmd_auto(Args())
        out = capsys.readouterr().out
        assert "Base64" in out


class TestMain:
    @patch("sys.argv", ["main.py", "encode", "hello"])
    def test_main_encode(self, capsys):
        main()
        out = capsys.readouterr().out
        assert len(out) > 0

    @patch("sys.argv", ["main.py", "decode", "aGVsbG8="])
    def test_main_decode(self, capsys):
        main()
        out = capsys.readouterr().out
        assert len(out) > 0

    @patch("sys.argv", ["main.py", "auto", "hello"])
    def test_main_auto(self, capsys):
        main()
        out = capsys.readouterr().out
        assert len(out) > 0

    @patch("sys.argv", ["main.py"])
    def test_main_no_command(self):
        with pytest.raises(SystemExit):
            main()


def test_main_block():
    script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
    with patch("sys.argv", ["main.py", "encode", "test"]):
        runpy.run_path(script, run_name="__main__")
