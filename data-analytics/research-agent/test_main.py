"""Tests for Research Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Research Agent" in result

    def test_run_mentions_research(self):
        result = run("")
        assert "research" in result.lower() or "topic" in result.lower()
