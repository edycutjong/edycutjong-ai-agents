"""Tests for Code Smell Detector agent."""
import pytest
from main import run, detect_smells


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
