"""Tests for License Auditor Agent."""
import pytest
from main import run, parse_requirements


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "License Auditor" in result


class TestParseRequirements:
    def test_parses_packages(self):
        text = "requests==2.28.0\nflask>=2.0\nnumpy\n"
        packages = parse_requirements(text)
        assert isinstance(packages, list)
        assert len(packages) > 0

    def test_empty_input(self):
        packages = parse_requirements("")
        assert isinstance(packages, list)
