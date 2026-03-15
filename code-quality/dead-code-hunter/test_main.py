"""Tests for Dead Code Hunter agent."""
import pytest
from main import run, find_unused_imports, find_unreachable


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
