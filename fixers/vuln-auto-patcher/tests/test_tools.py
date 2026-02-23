import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.audit import run_npm_audit, extract_vulnerabilities
from tools.patcher import get_installed_version, update_package
from tools.tester import run_tests

class TestAuditTools(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_npm_audit_success(self, mock_run):
        mock_run.return_value.stdout = json.dumps({"vulnerabilities": {}})
        mock_run.return_value.returncode = 0
        result = run_npm_audit()
        self.assertEqual(result, {"vulnerabilities": {}})

    @patch("subprocess.run")
    def test_run_npm_audit_error(self, mock_run):
        mock_run.return_value.stdout = "invalid json"
        mock_run.return_value.returncode = 1
        result = run_npm_audit()
        self.assertIn("error", result)

    def test_extract_vulnerabilities(self):
        report = {
            "vulnerabilities": {
                "lodash": {
                    "severity": "high",
                    "fixAvailable": True,
                    "range": "<4.17.19"
                }
            }
        }
        vulns = extract_vulnerabilities(report)
        self.assertEqual(len(vulns), 1)
        self.assertEqual(vulns[0]["package"], "lodash")
        self.assertEqual(vulns[0]["severity"], "high")

class TestPatcherTools(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_installed_version(self, mock_run):
        mock_run.return_value.stdout = json.dumps({
            "dependencies": {
                "react": {
                    "version": "16.8.0"
                }
            }
        })
        version = get_installed_version("react")
        self.assertEqual(version, "16.8.0")

    @patch("subprocess.run")
    def test_update_package(self, mock_run):
        mock_run.return_value.returncode = 0
        success = update_package("react", "16.9.0")
        self.assertTrue(success)

class TestTesterTools(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_tests_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Tests passed"
        result = run_tests()
        self.assertTrue(result["success"])
        self.assertEqual(result["stdout"], "Tests passed")

    @patch("subprocess.run")
    def test_run_tests_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "Tests failed"
        result = run_tests()
        self.assertFalse(result["success"])

if __name__ == "__main__":
    unittest.main()
