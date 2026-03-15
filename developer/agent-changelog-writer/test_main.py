"""Tests for Changelog Writer Agent."""
import pytest
from main import run, categorize_commits, generate_changelog


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Changelog Writer" in result


class TestCategorizeCommits:
    def test_categorizes_feat(self):
        cats = categorize_commits(["abc12345 feat: add login page"])
        assert len(cats["Added"]) == 1

    def test_categorizes_fix(self):
        cats = categorize_commits(["abc12345 fix: resolve crash"])
        assert len(cats["Fixed"]) == 1

    def test_categorizes_refactor(self):
        cats = categorize_commits(["abc12345 refactor: simplify auth"])
        assert len(cats["Changed"]) == 1

    def test_categorizes_remove(self):
        cats = categorize_commits(["abc12345 remove old endpoint"])
        assert len(cats["Removed"]) == 1

    def test_categorizes_security(self):
        cats = categorize_commits(["abc12345 security patch for CVE-2024"])
        assert len(cats["Security"]) == 1

    def test_unknown_goes_to_other(self):
        cats = categorize_commits(["abc12345 miscellaneous cleanup"])
        assert len(cats["Other"]) == 1


class TestGenerateChangelog:
    def test_generates_changelog_string(self):
        log = "abc12345 feat: add new API\ndef67890 fix: resolve bug"
        result = generate_changelog("1.0.0", log)
        assert "1.0.0" in result
        assert "Changelog" in result

    def test_includes_added_section(self):
        log = "abc12345 feat: add login"
        result = generate_changelog("1.0.0", log)
        assert "Added" in result
