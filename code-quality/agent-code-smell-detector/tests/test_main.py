"""Tests for code-smell-detector — targeting full main.py coverage."""
import sys, os, pytest, runpy
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import run, detect_smells, main


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Code Smell Detector" in result


class TestDetectSmells:
    def test_clean_code_no_smells(self):
        code = "def hello():\n    return 'world'\n"
        smells = detect_smells(code)
        assert any("No obvious code smells" in s for s in smells)

    def test_detects_magic_numbers(self):
        code = "x = 42\ny = 99\nz = 100\na = 200\nb = 300\n"
        smells = detect_smells(code)
        assert any("Magic numbers" in s for s in smells)

    def test_detects_long_lines(self):
        code = "x = " + "a" * 130 + "\n"
        smells = detect_smells(code)
        assert any("Long lines" in s for s in smells)

    def test_detects_deep_nesting(self):
        code = "if True:\n    if True:\n        if True:\n            if True:\n                if True:\n                    x = 1\n"
        smells = detect_smells(code)
        assert any("Deep nesting" in s for s in smells)

    def test_detects_long_function(self):
        lines = ["def big_func():"] + [f"    x{i} = {i}" for i in range(60)]
        code = "\n".join(lines) + "\n"
        smells = detect_smells(code)
        assert any("Long function" in s for s in smells)

    def test_returns_list(self):
        smells = detect_smells("x = 1\n")
        assert isinstance(smells, list)

    def test_syntax_error_handled(self):
        code = "def foo(\n"
        smells = detect_smells(code)
        assert isinstance(smells, list)

    def test_filename_param(self):
        code = "x = 1\n"
        smells = detect_smells(code, filename="test.py")
        assert isinstance(smells, list)


class TestMain:
    def test_no_file_arg(self):
        with patch('sys.argv', ['main']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_file_not_found(self):
        with patch('sys.argv', ['main', 'nonexistent_file.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_file_with_smells(self, tmp_path):
        code = "x = 42\ny = 99\nz = 100\na = 200\nb = 300\n"
        f = tmp_path / "smelly.py"
        f.write_text(code)
        with patch('sys.argv', ['main', str(f)]):
            main()  # should print report without error

    def test_clean_file(self, tmp_path):
        f = tmp_path / "clean.py"
        f.write_text("def hello():\n    return 'world'\n")
        with patch('sys.argv', ['main', str(f)]):
            main()

    def test_main_block(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("x = 1\n")
        with patch('sys.argv', ['main', str(f)]):
            runpy.run_module('main', run_name='__main__', alter_sys=True)
