"""Tests for Database Migration Reviewer agent."""
import pytest
from main import run, review_migration


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "DB Migration Reviewer" in result


class TestReviewMigration:
    def test_safe_migration(self):
        sql = "ALTER TABLE users ADD COLUMN bio TEXT;\n-- rollback\nALTER TABLE users DROP COLUMN bio;"
        findings = review_migration(sql)
        assert isinstance(findings, list)

    def test_detects_drop_table(self):
        findings = review_migration("DROP TABLE users;")
        assert any("DROP TABLE" in f for f in findings)

    def test_detects_truncate(self):
        findings = review_migration("TRUNCATE orders;")
        assert any("TRUNCATE" in f for f in findings)

    def test_detects_drop_database(self):
        findings = review_migration("DROP DATABASE production;")
        assert any("DROP DATABASE" in f for f in findings)

    def test_detects_delete_without_where(self):
        findings = review_migration("DELETE FROM users;")
        assert any("DELETE" in f for f in findings)

    def test_detects_not_null_without_default(self):
        findings = review_migration("ALTER TABLE users ADD COLUMN age INT NOT NULL;")
        assert any("NOT NULL" in f for f in findings)

    def test_warns_missing_rollback(self):
        findings = review_migration("ALTER TABLE users ADD COLUMN name TEXT;")
        assert any("rollback" in f.lower() for f in findings)

    def test_rollback_present_no_warning(self):
        sql = "ALTER TABLE users ADD COLUMN name TEXT;\n-- rollback\nALTER TABLE users DROP COLUMN name;"
        findings = review_migration(sql)
        assert not any("rollback" in f.lower() and "MEDIUM" in f for f in findings)
