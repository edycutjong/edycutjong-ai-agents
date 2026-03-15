"""Tests for Git Workflow Agent."""
import pytest
from main import run


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Git Workflow Agent" in result

    def test_run_mentions_workflow(self):
        result = run("")
        assert "workflow" in result.lower() or "git" in result.lower()
