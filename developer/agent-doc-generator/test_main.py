"""Tests for Doc Generator Agent."""
import pytest
from main import run, extract_docstrings


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Doc Generator" in result


class TestExtractDocstrings:
    def test_extracts_function_with_docstring(self):
        code = 'def add(a, b):\n    """Add two numbers."""\n    return a + b\n'
        results = extract_docstrings(code)
        assert isinstance(results, list)

    def test_extracts_function_without_docstring(self):
        code = "def add(a, b):\n    return a + b\n"
        results = extract_docstrings(code)
        assert isinstance(results, list)
