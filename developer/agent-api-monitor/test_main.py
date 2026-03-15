"""Tests for API Monitor Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "API Monitor" in result
