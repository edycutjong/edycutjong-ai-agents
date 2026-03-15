"""Tests for Migration Checker Agent."""
import pytest
from main import run, check_migration


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Migration Checker" in result


class TestCheckMigration:
    def test_safe_migration(self):
        sql = "ALTER TABLE users ADD COLUMN bio TEXT;"
        issues = check_migration(sql)
        assert any("No obvious" in i or "✅" in i for i in issues)

    def test_detects_drop_table(self):
        issues = check_migration("DROP TABLE users;")
        assert any("DROP TABLE" in i for i in issues)

    def test_detects_drop_column(self):
        issues = check_migration("ALTER TABLE users DROP COLUMN email;")
        assert any("DROP COLUMN" in i for i in issues)

    def test_detects_truncate(self):
        issues = check_migration("TRUNCATE orders;")
        assert any("TRUNCATE" in i for i in issues)

    def test_detects_missing_primary_key(self):
        issues = check_migration("CREATE TABLE users (name TEXT);")
        assert any("PRIMARY KEY" in i for i in issues)

    def test_returns_list(self):
        result = check_migration("SELECT 1;")
        assert isinstance(result, list)
