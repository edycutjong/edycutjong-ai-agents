"""Tests for AI Code Review Agent."""
import pytest
from main import run, review_code


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "AI Code Review" in result


class TestReviewCode:
    def test_clean_code_no_issues(self):
        code = "def add(a, b):\n    return a + b\n"
        issues = review_code(code)
        assert any("No common issues" in i for i in issues)

    def test_detects_print_statement(self):
        code = "print('debug')\n"
        issues = review_code(code)
        assert any("Debug print" in i for i in issues)

    def test_detects_eval_usage(self):
        code = "result = eval('1+1')\n"
        issues = review_code(code)
        assert any("eval()" in i for i in issues)

    def test_detects_bare_except(self):
        code = "try:\n    x = 1\nexcept:\n    pass\n"
        issues = review_code(code)
        assert any("Bare except" in i or "swallows" in i for i in issues)

    def test_detects_global_usage(self):
        code = "global my_var\n"
        issues = review_code(code)
        assert any("Global" in i for i in issues)

    def test_detects_range_len(self):
        code = "for i in range(len(items)):\n    pass\n"
        issues = review_code(code)
        assert any("enumerate" in i for i in issues)

    def test_detects_len_equals_zero(self):
        code = "if len(items) == 0:\n    pass\n"
        issues = review_code(code)
        assert any("not collection" in i for i in issues)

    def test_returns_list(self):
        assert isinstance(review_code("x = 1"), list)
