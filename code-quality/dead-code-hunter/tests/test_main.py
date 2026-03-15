"""Tests for Dead Code Hunter agent."""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, mock_open
import runpy
import os
from main import run, find_unused_imports, find_unreachable, main


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Dead Code Hunter" in result


class TestFindUnusedImports:
    def test_no_unused(self):
        code = "import os\npath = os.getcwd()\n"
        issues = find_unused_imports(code)
        assert issues == []

    def test_detects_unused_import(self):
        code = "import os\nimport sys\nx = 1\n"
        issues = find_unused_imports(code)
        assert any("os" in i for i in issues)
        assert any("sys" in i for i in issues)

    def test_handles_syntax_error(self):
        code = "def broken(\n"
        issues = find_unused_imports(code)
        assert any("Syntax error" in i for i in issues)

    def test_aliased_import_used(self):
        code = "import numpy as np\nx = np.array([1])\n"
        issues = find_unused_imports(code)
        assert issues == []
        
    def test_import_from_unused(self):
        code = "from collections import defaultdict\nfrom typing import List as L\n"
        issues = find_unused_imports(code)
        assert any("defaultdict" in i for i in issues)
        assert any("L" in i for i in issues)


class TestFindUnreachable:
    def test_no_unreachable(self):
        code = "def foo():\n    return 1\n"
        issues = find_unreachable(code)
        assert issues == []

    def test_detects_code_after_return(self):
        code = "def foo():\n    return 1\n    x = 2\n"
        issues = find_unreachable(code)
        assert any("unreachable" in i.lower() for i in issues)

    def test_new_function_resets(self):
        code = "def foo():\n    return 1\ndef bar():\n    x = 2\n"
        issues = find_unreachable(code)
        assert issues == []


class TestMainCli:
    @patch("sys.argv", ["main.py"])
    def test_no_args(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        out, _ = capsys.readouterr()
        assert "Usage: python main.py <source.py>" in out

    @patch("sys.argv", ["main.py", "doesnt_exist.py"])
    @patch("os.path.isfile", return_value=False)
    def test_file_not_found(self, mock_isfile, capsys):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        out, _ = capsys.readouterr()
        assert "File not found" in out

    @patch("sys.argv", ["main.py", "test_file.py"])
    @patch("os.path.isfile", return_value=True)
    def test_main_with_issues(self, mock_isfile, capsys):
        code = "import os\ndef test():\n    return 1\n    print('dead')\n"
        with patch("builtins.open", mock_open(read_data=code)):
            main()
        out, _ = capsys.readouterr()
        assert "Dead Code Report" in out
        assert "Unused import: 'os'" in out
        assert "Potential unreachable code" in out
        
    @patch("sys.argv", ["main.py", "test_clean.py"])
    @patch("os.path.isfile", return_value=True)
    def test_main_no_issues(self, mock_isfile, capsys):
        code = "def test():\n    return 1\n"
        with patch("builtins.open", mock_open(read_data=code)):
            main()
        out, _ = capsys.readouterr()
        assert "Dead Code Report: test_clean.py" in out
        assert "No dead code detected." in out

    @patch("sys.argv", ["main.py", "test_file.py"])
    @patch("os.path.isfile", return_value=True)
    def test_main_dunder(self, mock_isfile):
        # Test __main__ block
        code = "def test():\n    return 1\n"
        with patch("builtins.open", mock_open(read_data=code)):
            with patch("sys.argv", ["main.py", "test_file.py"]):
                runpy.run_path("main.py", run_name="__main__")
