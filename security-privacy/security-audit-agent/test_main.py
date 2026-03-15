"""Tests for Security Audit Agent."""
import pytest
import re
from main import run, VULNS


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Security Audit" in result


class TestVulnPatterns:
    """Test the VULNS patterns directly."""

    def test_detects_eval(self):
        code = "result = eval(user_input)"
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert any("eval" in msg.lower() for _, msg in matches)

    def test_detects_pickle_loads(self):
        code = "data = pickle.loads(payload)"
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert any("pickle" in msg.lower() for _, msg in matches)

    def test_detects_shell_true(self):
        code = "subprocess.call('ls', shell=True)"
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert any("shell" in msg.lower() for _, msg in matches)

    def test_detects_hardcoded_password(self):
        code = '"password": "hunter2"'
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert any("password" in msg.lower() or "Hardcoded" in msg for _, msg in matches)

    def test_detects_debug_mode(self):
        code = "DEBUG = True"
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert any("Debug" in msg or "debug" in msg.lower() for _, msg in matches)

    def test_detects_ssl_verify_disabled(self):
        code = "verify = False"
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert any("SSL" in msg or "MITM" in msg for _, msg in matches)

    def test_clean_code_no_vulns(self):
        code = "def add(a, b):\n    return a + b"
        matches = [(sev, msg) for pat, sev, msg in VULNS if re.search(pat, code)]
        assert len(matches) == 0
