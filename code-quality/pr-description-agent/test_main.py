"""Tests for PR Description Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "PR Description Agent" in result

    def test_run_mentions_diff(self):
        result = run("")
        assert "diff" in result.lower() or "PR" in result
