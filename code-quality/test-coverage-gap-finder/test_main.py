"""Tests for Test Coverage Gap Finder agent."""
import pytest
from main import run, get_functions, get_tested_functions


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Coverage Gap Finder" in result


class TestGetFunctions:
    def test_extracts_functions(self):
        code = "def add(a, b):\n    return a + b\ndef sub(a, b):\n    return a - b\n"
        fns = get_functions(code)
        assert "add" in fns
        assert "sub" in fns

    def test_ignores_private_functions(self):
        code = "def _helper():\n    pass\ndef public():\n    pass\n"
        fns = get_functions(code)
        assert "_helper" not in fns
        assert "public" in fns

    def test_empty_code(self):
        fns = get_functions("x = 1\n")
        assert fns == set()

    def test_handles_syntax_error(self):
        fns = get_functions("def broken(\n")
        assert isinstance(fns, set)


class TestGetTestedFunctions:
    def test_extracts_test_names(self):
        test_code = "def test_add():\n    pass\ndef test_sub():\n    pass\n"
        tested = get_tested_functions(test_code)
        assert "add" in tested
        assert "sub" in tested

    def test_extracts_function_calls(self):
        test_code = "result = add(1, 2)\nassert result == 3\n"
        tested = get_tested_functions(test_code)
        assert "add" in tested
