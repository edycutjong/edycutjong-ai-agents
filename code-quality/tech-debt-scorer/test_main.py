"""Tests for Tech Debt Scorer agent."""
import pytest
from main import run, score_file, grade


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Tech Debt Scorer" in result


class TestScoreFile:
    def test_clean_code_low_score(self):
        code = '"""Module docstring."""\ndef add(a, b):\n    """Add two numbers."""\n    return a + b\n'
        score, findings = score_file(code)
        assert score <= 5

    def test_todo_increases_score(self):
        code = "# TODO: fix this\n# TODO: refactor\n"
        score, findings = score_file(code)
        assert score >= 2

    def test_hack_increases_score(self):
        code = "# HACK: workaround for bug\n"
        score, findings = score_file(code)
        assert score >= 3

    def test_eval_high_penalty(self):
        code = "x = eval('1+1')\n"
        score, findings = score_file(code)
        assert score >= 5

    def test_returns_tuple(self):
        score, findings = score_file("x = 1\n")
        assert isinstance(score, int)
        assert isinstance(findings, list)

    def test_score_never_negative(self):
        code = '"""Great docstring."""\n'
        score, findings = score_file(code)
        assert score >= 0


class TestGrade:
    def test_grade_a(self):
        assert "A" in grade(0)

    def test_grade_b(self):
        assert "B" in grade(10)

    def test_grade_c(self):
        assert "C" in grade(25)

    def test_grade_d(self):
        assert "D" in grade(40)

    def test_grade_f(self):
        assert "F" in grade(100)
