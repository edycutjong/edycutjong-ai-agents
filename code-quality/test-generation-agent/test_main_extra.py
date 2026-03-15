"""Tests for Test Generation Agent — main() and __main__ block coverage."""
import os, sys, runpy
from unittest.mock import patch
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import main


class TestMainNoFile:
    @patch("sys.argv", ["main.py"])
    def test_main_no_file(self):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


class TestMainWithFile:
    def test_main_with_real_file(self, capsys, tmp_path):
        source = tmp_path / "sample.py"
        source.write_text("def add(a, b):\n    return a + b\n")
        with patch("sys.argv", ["main.py", str(source)]):
            main()
        out = capsys.readouterr().out
        assert "test_add" in out

    def test_main_with_output(self, capsys, tmp_path):
        source = tmp_path / "sample.py"
        source.write_text("def greet(name):\n    print(name)\n")
        output_file = tmp_path / "test_output.py"
        with patch("sys.argv", ["main.py", str(source), "--output", str(output_file)]):
            main()
        out = capsys.readouterr().out
        assert "Tests written to" in out
        assert output_file.exists()

    def test_main_file_not_found(self):
        with patch("sys.argv", ["main.py", "/nonexistent/file.py"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_no_functions(self, capsys, tmp_path):
        source = tmp_path / "empty.py"
        source.write_text("# just a comment\nx = 42\n")
        with patch("sys.argv", ["main.py", str(source)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0


def test_main_block():
    script = os.path.join(os.path.dirname(__file__), "main.py")
    with patch("sys.argv", ["main.py"]):
        with pytest.raises(SystemExit):
            runpy.run_path(script, run_name="__main__")
