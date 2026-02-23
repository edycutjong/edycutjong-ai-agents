"""Tests for Secret Scanner."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.scanner import scan_text, scan_file, scan_directory, get_severity_counts, format_report_markdown, SECRET_PATTERNS

def test_detect_aws_key():
    m = scan_text('aws_key = "AKIAIOSFODNN7EXAMPLE"')
    assert any("AWS" in x.rule for x in m)

def test_detect_github_token():
    m = scan_text('token = "ghp_ABCDEFGHIJKLMNOPabcdefghijklmnop1234567"')
    assert any("GitHub" in x.rule for x in m)

def test_detect_generic_api_key():
    m = scan_text('api_key = "abcdefghij1234567890ABCD"')
    assert any("API Key" in x.rule for x in m)

def test_detect_password():
    m = scan_text('password = "mySuperSecretPassword123"')
    assert any("Secret" in x.rule for x in m)

def test_detect_jwt():
    m = scan_text('token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"')
    assert any("JWT" in x.rule for x in m)

def test_detect_private_key():
    m = scan_text('-----BEGIN RSA PRIVATE KEY-----')
    assert any("Private Key" in x.rule for x in m)

def test_detect_stripe():
    m = scan_text('key = "sk_test_EXAMPLE_KEY_REDACTED_000000"')
    assert any("Stripe" in x.rule for x in m)

def test_detect_db_url():
    m = scan_text('DATABASE_URL = "postgres://user:pass@host:5432/db"')
    assert any("Database" in x.rule for x in m)

def test_no_false_positive():
    m = scan_text('hello = "world"')
    assert len(m) == 0

def test_skip_comments():
    m = scan_text('# api_key = "abcdefghij1234567890ABCD"')
    assert len(m) == 0

def test_severity_counts():
    m = scan_text('AKIAIOSFODNN7EXAMPLE and password = "supersecret1234"')
    counts = get_severity_counts(m)
    assert counts["critical"] >= 1 or counts["high"] >= 1

def test_masking():
    m = scan_text('api_key = "abcdefghij1234567890ABCD"')
    if m:
        d = m[0].to_dict()
        assert "****" in d["match_masked"]

def test_scan_file(tmp_path):
    f = tmp_path / "test.py"
    f.write_text('secret = "mySuperSecretPassword123"\n')
    matches = scan_file(str(f))
    assert len(matches) >= 1

def test_scan_directory(tmp_path):
    f = tmp_path / "config.py"
    f.write_text('api_key = "abcdefghij1234567890ABCD"\n')
    matches = scan_directory(str(tmp_path))
    assert len(matches) >= 1

def test_format_clean():
    md = format_report_markdown([])
    assert "No secrets" in md

def test_format_findings():
    m = scan_text('AKIAIOSFODNN7EXAMPLE')
    md = format_report_markdown(m)
    assert "Report" in md

def test_patterns_count():
    assert len(SECRET_PATTERNS) >= 10
