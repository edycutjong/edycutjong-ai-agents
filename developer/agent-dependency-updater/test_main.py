"""Tests for Dependency Updater Agent."""
import pytest
from main import run, parse_requirements


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Dependency" in result or "dependency" in result.lower()


class TestParseRequirements:
    def test_parses_simple_requirements(self):
        text = "requests==2.28.0\nflask>=2.0\nnumpy"
        result = parse_requirements(text)
        assert isinstance(result, dict)

    def test_empty_text(self):
        result = parse_requirements("")
        assert isinstance(result, dict)
