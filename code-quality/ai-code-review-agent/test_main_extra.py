"""Tests for AI Code Review Agent — main() and __main__ block coverage."""
import os, sys, runpy, tempfile
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import main, review_code


class TestMainNoFile:
    @patch("sys.argv", ["main.py"])
    def test_main_no_file(self):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


class TestMainWithFile:
    def test_main_with_real_file(self, capsys, tmp_path):
        source = tmp_path / "sample.py"
        source.write_text("x = eval('1+1')\n")
        with patch("sys.argv", ["main.py", str(source)]):
            main()
        out = capsys.readouterr().out
        assert "eval()" in out

    def test_main_with_inline_code(self, capsys):
        with patch("sys.argv", ["main.py", "global my_var"]):
            main()
        out = capsys.readouterr().out
        assert "Global" in out

    def test_main_clean_file(self, capsys, tmp_path):
        source = tmp_path / "clean.py"
        source.write_text("def add(a, b):\n    return a + b\n")
        with patch("sys.argv", ["main.py", str(source)]):
            main()
        out = capsys.readouterr().out
        assert "No common issues" in out


def test_main_block():
    script = os.path.join(os.path.dirname(__file__), "main.py")
    with patch("sys.argv", ["main.py"]):
        with pytest.raises(SystemExit):
            runpy.run_path(script, run_name="__main__")
