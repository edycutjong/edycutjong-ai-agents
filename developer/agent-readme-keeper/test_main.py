"""Tests for README Keeper Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "README Keeper" in result
