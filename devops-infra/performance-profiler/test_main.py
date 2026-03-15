"""Tests for Performance Profiler Agent."""
import pytest
import re
from main import run, PERF_ISSUES


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Performance Profiler" in result


class TestPerfIssuePatterns:
    """Test the PERF_ISSUES patterns directly."""

    def test_detects_blocking_sleep(self):
        code = "time.sleep(5)"
        matches = [msg for pat, msg in PERF_ISSUES if re.search(pat, code, re.IGNORECASE)]
        assert any("sleep" in m.lower() for m in matches)

    def test_detects_select_star(self):
        code = "SELECT * FROM users"
        matches = [msg for pat, msg in PERF_ISSUES if re.search(pat, code, re.IGNORECASE)]
        assert any("SELECT" in m for m in matches)

    def test_detects_string_concat(self):
        code = "result += 'hello'"
        matches = [msg for pat, msg in PERF_ISSUES if re.search(pat, code, re.IGNORECASE)]
        assert any("concatenation" in m.lower() or "join" in m.lower() for m in matches)

    def test_clean_code_no_issues(self):
        code = "x = add(1, 2)"
        matches = [msg for pat, msg in PERF_ISSUES if re.search(pat, code, re.IGNORECASE)]
        assert len(matches) == 0
