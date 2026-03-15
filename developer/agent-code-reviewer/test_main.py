"""Tests for Code Reviewer Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Code Review" in result or "code review" in result.lower()
