"""Tests for Refactoring Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Refactoring Agent" in result

    def test_run_mentions_refactoring(self):
        result = run("")
        assert "refactoring" in result.lower()
