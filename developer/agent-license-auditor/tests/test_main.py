"""Tests for the License Auditor Agent."""
import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import (
    normalize_license, check_blocked, get_installed_licenses,
    audit_licenses, format_markdown, format_csv, print_console_report
)


class TestNormalizeLicense:
    def test_string_license(self):
        assert normalize_license("MIT") == "MIT"

    def test_list_license(self):
        assert normalize_license(["MIT", "ISC"]) == "MIT, ISC"

    def test_none_license(self):
        assert normalize_license(None) == "UNKNOWN"

    def test_empty_string(self):
        assert normalize_license("") == "UNKNOWN"

    def test_whitespace_string(self):
        assert normalize_license("  ") == "UNKNOWN"


class TestCheckBlocked:
    def test_blocked_gpl(self):
        assert check_blocked("GPL-3.0", ["GPL", "AGPL"]) is True

    def test_not_blocked_mit(self):
        assert check_blocked("MIT", ["GPL", "AGPL"]) is False

    def test_case_insensitive(self):
        assert check_blocked("gpl-3.0", ["GPL"]) is True

    def test_empty_block_list(self):
        assert check_blocked("GPL-3.0", []) is False

    def test_agpl_blocked(self):
        assert check_blocked("AGPL-3.0", ["AGPL"]) is True


class TestAuditLicenses:
    def test_all_ok(self):
        packages = [
            {"package": "pkg@1.0", "name": "pkg", "version": "1.0",
             "license": "MIT", "repository": "N/A", "author": "N/A"}
        ]
        data, blocked, unknown = audit_licenses(packages, ["GPL"], [])
        assert data[0]["status"] == "OK"
        assert blocked == 0
        assert unknown == 0

    def test_blocked_license(self):
        packages = [
            {"package": "pkg@1.0", "name": "pkg", "version": "1.0",
             "license": "GPL-3.0", "repository": "N/A", "author": "N/A"}
        ]
        data, blocked, unknown = audit_licenses(packages, ["GPL"], [])
        assert data[0]["status"] == "BLOCKED_LICENSE"
        assert blocked == 1

    def test_unknown_license(self):
        packages = [
            {"package": "pkg@1.0", "name": "pkg", "version": "1.0",
             "license": "UNKNOWN", "repository": "N/A", "author": "N/A"}
        ]
        data, blocked, unknown = audit_licenses(packages, ["GPL"], [])
        assert data[0]["status"] == "MISSING_LICENSE"
        assert unknown == 1

    def test_not_in_allow_list(self):
        packages = [
            {"package": "pkg@1.0", "name": "pkg", "version": "1.0",
             "license": "Apache-2.0", "repository": "N/A", "author": "N/A"}
        ]
        data, blocked, unknown = audit_licenses(packages, [], ["MIT"])
        assert data[0]["status"] == "NOT_ALLOWED_LICENSE"
        assert blocked == 1


class TestFormatMarkdown:
    def test_markdown_output(self):
        data = [{"package": "pkg@1.0", "license": "MIT", "status": "OK", "repository": "N/A", "author": "N/A"}]
        md = format_markdown(data)
        assert "# Third-Party Licenses" in md
        assert "| pkg@1.0 | MIT | OK | N/A |" in md


class TestFormatCsv:
    def test_csv_output(self):
        data = [{"package": "pkg@1.0", "license": "MIT", "status": "OK", "repository": "N/A", "author": "N/A"}]
        csv_str = format_csv(data)
        assert "package,license,status,repository" in csv_str
        assert "pkg@1.0,MIT,OK,N/A" in csv_str


class TestPrintConsoleReport:
    def test_clean_report(self, capsys):
        data = [{"package": "pkg@1.0", "license": "MIT", "status": "OK"}]
        print_console_report(data, 0, 0)
        output = capsys.readouterr().out
        assert "All dependencies align" in output

    def test_report_with_issues(self, capsys):
        data = [{"package": "pkg@1.0", "license": "GPL-3.0", "status": "BLOCKED_LICENSE"}]
        print_console_report(data, 1, 0)
        output = capsys.readouterr().out
        assert "BLOCKED_LICENSE" in output
        assert "1 packages with blocked" in output
