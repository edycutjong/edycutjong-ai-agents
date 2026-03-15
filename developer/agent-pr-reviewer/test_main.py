"""Tests for PR Reviewer Agent."""
import pytest
from main import run, parse_diff_stats, basic_lint_review


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "PR Reviewer" in result


class TestParseDiffStats:
    def test_counts_additions(self):
        diff = "+new line 1\n+new line 2\n"
        stats = parse_diff_stats(diff)
        assert stats["additions"] == 2

    def test_counts_deletions(self):
        diff = "-old line 1\n-old line 2\n-old line 3\n"
        stats = parse_diff_stats(diff)
        assert stats["deletions"] == 3

    def test_extracts_files(self):
        diff = "diff --git a/src/app.py b/src/app.py\n+x = 1\n"
        stats = parse_diff_stats(diff)
        assert "src/app.py" in stats["files"]


class TestBasicLintReview:
    def test_detects_todo(self):
        issues = basic_lint_review("# TODO: fix this")
        assert any("TODO" in i for i in issues)

    def test_detects_debug_statements(self):
        issues = basic_lint_review("console.log('debug')")
        assert any("Debug" in i or "debug" in i.lower() for i in issues)

    def test_detects_secrets(self):
        issues = basic_lint_review("password = 'hunter2'")
        assert any("secret" in i.lower() or "password" in i.lower() for i in issues)

    def test_detects_eval(self):
        issues = basic_lint_review("result = eval(user_input)")
        assert any("eval" in i.lower() for i in issues)

    def test_clean_diff(self):
        issues = basic_lint_review("def add(a, b):\n    return a + b")
        assert any("✅" in i or "No obvious" in i for i in issues)
