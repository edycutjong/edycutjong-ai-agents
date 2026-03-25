"""Tests for the Dependency Updater Agent."""
import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import get_outdated, install_package, run_tests, rollback_package, update_dependencies, format_report


class TestGetOutdated:
    @patch("main.subprocess.run")
    def test_returns_outdated_packages(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps([
                {"name": "requests", "version": "2.28.0", "latest_version": "2.31.0"},
                {"name": "flask", "version": "2.3.0", "latest_version": "3.0.0"},
            ])
        )
        result = get_outdated("/fake/dir")
        assert len(result) == 2
        assert result[0]["name"] == "requests"

    @patch("main.subprocess.run")
    def test_returns_empty_on_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        result = get_outdated("/fake/dir")
        assert result == []

    @patch("main.subprocess.run")
    def test_returns_empty_on_bad_json(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="not json")
        result = get_outdated("/fake/dir")
        assert result == []


class TestInstallPackage:
    @patch("main.subprocess.run")
    def test_successful_install(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")
        success, output = install_package("requests", "2.31.0", "/fake")
        assert success is True

    @patch("main.subprocess.run")
    def test_failed_install(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
        success, output = install_package("badpkg", "1.0.0", "/fake")
        assert success is False


class TestRunTests:
    @patch("main.subprocess.run")
    def test_tests_pass(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="passed", stderr="")
        success, output = run_tests("python -m pytest", "/fake")
        assert success is True

    @patch("main.subprocess.run")
    def test_tests_fail(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stdout="FAILED", stderr="")
        success, output = run_tests("python -m pytest", "/fake")
        assert success is False


class TestUpdateDependencies:
    @patch("main.rollback_package")
    @patch("main.run_tests")
    @patch("main.install_package")
    @patch("main.get_outdated")
    def test_all_up_to_date(self, mock_outdated, mock_install, mock_tests, mock_rollback):
        mock_outdated.return_value = []
        report = update_dependencies("/fake")
        assert report["success"] == []
        assert report["failed"] == []

    @patch("main.rollback_package")
    @patch("main.run_tests")
    @patch("main.install_package")
    @patch("main.get_outdated")
    def test_successful_update(self, mock_outdated, mock_install, mock_tests, mock_rollback):
        mock_outdated.return_value = [
            {"name": "requests", "version": "2.28.0", "latest_version": "2.31.0"}
        ]
        mock_install.return_value = (True, "OK")
        mock_tests.return_value = (True, "passed")
        report = update_dependencies("/fake")
        assert len(report["success"]) == 1
        assert report["success"][0]["package"] == "requests"

    @patch("main.rollback_package")
    @patch("main.run_tests")
    @patch("main.install_package")
    @patch("main.get_outdated")
    def test_rollback_on_test_failure(self, mock_outdated, mock_install, mock_tests, mock_rollback):
        mock_outdated.return_value = [
            {"name": "badpkg", "version": "1.0.0", "latest_version": "2.0.0"}
        ]
        mock_install.return_value = (True, "OK")
        mock_tests.return_value = (False, "FAILED")
        mock_rollback.return_value = True
        report = update_dependencies("/fake")
        assert len(report["failed"]) == 1
        assert report["failed"][0]["reason"] == "Tests failed"
        mock_rollback.assert_called_once()

    @patch("main.rollback_package")
    @patch("main.run_tests")
    @patch("main.install_package")
    @patch("main.get_outdated")
    def test_ignore_list(self, mock_outdated, mock_install, mock_tests, mock_rollback):
        mock_outdated.return_value = [
            {"name": "skip-me", "version": "1.0.0", "latest_version": "2.0.0"}
        ]
        report = update_dependencies("/fake", ignore=["skip-me"])
        assert len(report["skipped"]) == 1
        mock_install.assert_not_called()


class TestFormatReport:
    def test_empty_report(self):
        report = {"success": [], "failed": [], "skipped": []}
        output = format_report(report)
        assert "Successfully updated: 0" in output

    def test_report_with_results(self):
        report = {
            "success": [{"package": "requests", "from": "2.28", "to": "2.31"}],
            "failed": [{"package": "bad", "reason": "Tests failed"}],
            "skipped": [],
        }
        output = format_report(report)
        assert "Successfully updated: 1" in output
        assert "Failed (rolled back): 1" in output
        assert "requests" in output
