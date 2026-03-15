"""Tests for Issue Labeler Agent."""
import pytest
from main import run, suggest_labels


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Issue Labeler" in result


class TestSuggestLabels:
    def test_bug_label(self):
        labels = suggest_labels("App crashes on login", "Error: null pointer")
        assert "bug" in labels

    def test_feature_label(self):
        labels = suggest_labels("Add dark mode support", "Feature request")
        assert "feature" in labels

    def test_documentation_label(self):
        labels = suggest_labels("Typo in README", "Fix spelling in docs")
        assert "documentation" in labels

    def test_security_label(self):
        labels = suggest_labels("XSS vulnerability in form", "Security issue")
        assert "security" in labels

    def test_performance_label(self):
        labels = suggest_labels("Page loads slowly", "Performance issue")
        assert "performance" in labels

    def test_question_label(self):
        labels = suggest_labels("How to configure auth?", "Help needed")
        assert "question" in labels

    def test_no_match_returns_needs_triage(self):
        labels = suggest_labels("Miscellaneous", "Just some text")
        assert "needs-triage" in labels

    def test_returns_list(self):
        result = suggest_labels("test", "body")
        assert isinstance(result, list)
