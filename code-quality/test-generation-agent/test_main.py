"""Tests for Test Generation Agent."""
import pytest
from main import run, extract_functions, gen_tests


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Test Generation Agent" in result


class TestExtractFunctions:
    def test_extracts_simple_function(self):
        code = "def add(a, b):\n    return a + b\n"
        fns = extract_functions(code)
        assert len(fns) == 1
        assert fns[0]["name"] == "add"
        assert fns[0]["params"] == ["a", "b"]
        assert fns[0]["has_return"] is True

    def test_extracts_no_return(self):
        code = "def greet(name):\n    print(name)\n"
        fns = extract_functions(code)
        assert fns[0]["has_return"] is False

    def test_extracts_multiple(self):
        code = "def foo():\n    pass\ndef bar(x):\n    return x\n"
        fns = extract_functions(code)
        assert len(fns) == 2

    def test_handles_syntax_error(self):
        code = "def broken(\n"
        fns = extract_functions(code)
        assert isinstance(fns, list)

    def test_ignores_self_param(self):
        code = "class A:\n    def method(self, x):\n        return x\n"
        fns = extract_functions(code)
        method = [f for f in fns if f["name"] == "method"][0]
        assert "self" not in method["params"]


class TestGenTests:
    def test_generates_test_code(self):
        fns = [{"name": "add", "params": ["a", "b"], "has_return": True}]
        result = gen_tests(fns, "math_utils")
        assert "test_add" in result
        assert "import pytest" in result

    def test_generates_class_name(self):
        fns = [{"name": "my_func", "params": [], "has_return": False}]
        result = gen_tests(fns, "module")
        assert "TestMyFunc" in result or "TestMy_func" in result

    def test_includes_edge_case(self):
        fns = [{"name": "process", "params": ["data"], "has_return": True}]
        result = gen_tests(fns, "mod")
        assert "edge_case" in result
