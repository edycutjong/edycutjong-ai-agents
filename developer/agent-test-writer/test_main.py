"""Tests for Test Writer Agent."""
import pytest
from main import run, extract_python_functions, generate_stub_tests


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Test Writer" in result


class TestExtractPythonFunctions:
    def test_extracts_function(self):
        code = "def add(a, b):\n    return a + b\n"
        fns = extract_python_functions(code)
        assert len(fns) >= 1
        assert fns[0][0] == "add"

    def test_empty_code(self):
        fns = extract_python_functions("x = 1\n")
        assert fns == []


class TestGenerateStubTests:
    def test_generates_tests(self):
        fns = [("add", "def add(a, b)")]
        result = generate_stub_tests(fns, "math_module")
        assert "test_add" in result

    def test_uses_module_name(self):
        fns = [("foo", "def foo()")]
        result = generate_stub_tests(fns, "my_mod")
        assert "my_mod" in result
