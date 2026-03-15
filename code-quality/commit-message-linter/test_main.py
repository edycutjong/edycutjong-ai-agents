"""Tests for Commit Message Linter agent."""
import pytest
from main import run, lint_message, TYPES


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Commit Linter" in result


class TestLintMessage:
    def test_valid_message(self):
        result = lint_message("feat(auth): add OAuth2 login")
        assert any("Valid" in r for r in result)

    def test_valid_fix_message(self):
        result = lint_message("fix: resolve crash on startup")
        assert any("Valid" in r for r in result)

    def test_invalid_format(self):
        result = lint_message("Updated the readme file")
        assert any("❌" in r for r in result)

    def test_unknown_type(self):
        result = lint_message("yolo(scope): did something")
        assert any("Unknown type" in r for r in result)

    def test_uppercase_description(self):
        result = lint_message("feat: Add new feature")
        assert any("lowercase" in r for r in result)

    def test_trailing_period(self):
        result = lint_message("fix: resolve bug.")
        assert any("period" in r for r in result)

    def test_subject_too_long(self):
        result = lint_message("feat: " + "a" * 80)
        assert any("too long" in r for r in result)

    def test_breaking_change(self):
        result = lint_message("feat!: remove deprecated API")
        assert any("BREAKING" in r for r in result)

    def test_all_types_are_valid(self):
        for t in TYPES:
            result = lint_message(f"{t}: do something")
            assert not any("Unknown type" in r for r in result)
