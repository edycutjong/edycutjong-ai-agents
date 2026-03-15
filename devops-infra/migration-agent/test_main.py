"""Tests for Migration Agent."""
import pytest
import re
from main import run, RISKS


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Migration Agent" in result


class TestRisksPatterns:
    """Test the RISKS patterns directly since main() reads from files."""

    def test_detects_drop_table(self):
        sql = "DROP TABLE users;"
        matches = [msg for pat, msg in RISKS if re.search(pat, sql, re.IGNORECASE)]
        assert any("DROP TABLE" in m for m in matches)

    def test_detects_truncate(self):
        sql = "TRUNCATE orders;"
        matches = [msg for pat, msg in RISKS if re.search(pat, sql, re.IGNORECASE)]
        assert any("TRUNCATE" in m for m in matches)

    def test_detects_drop_column(self):
        sql = "ALTER TABLE users DROP COLUMN email;"
        matches = [msg for pat, msg in RISKS if re.search(pat, sql, re.IGNORECASE)]
        assert any("DROP COLUMN" in m for m in matches)

    def test_safe_sql_no_match(self):
        sql = "ALTER TABLE users ADD COLUMN bio TEXT;"
        matches = [msg for pat, msg in RISKS if re.search(pat, sql, re.IGNORECASE)]
        assert len(matches) == 0
