"""Tests for PR Description Writer agent."""
import pytest
from main import run, generate_pr_description


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "PR Description Writer" in result


class TestGeneratePrDescription:
    def test_generates_description(self):
        desc = generate_pr_description("Added a new login page")
        assert "Summary" in desc
        assert "Changes" in desc

    def test_counts_added_lines(self):
        diff = "+new line 1\n+new line 2\n-old line\n"
        desc = generate_pr_description(diff)
        assert "2 lines added" in desc
        assert "1 lines removed" in desc

    def test_extracts_files_from_diff(self):
        diff = "diff --git a/src/app.py b/src/app.py\n+x = 1\n"
        desc = generate_pr_description(diff)
        assert "src/app.py" in desc

    def test_no_diff_zero_counts(self):
        desc = generate_pr_description("Just a text description")
        assert "0 lines added" in desc

    def test_includes_testing_section(self):
        desc = generate_pr_description("fix: resolve bug")
        assert "Testing" in desc

    def test_includes_type_of_change(self):
        desc = generate_pr_description("feature work")
        assert "Type of Change" in desc
