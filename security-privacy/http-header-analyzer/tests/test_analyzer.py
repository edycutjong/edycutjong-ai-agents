"""Tests for HTTP Header Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import analyze_headers, format_result_markdown, SECURITY_HEADERS

GOOD = {"Strict-Transport-Security": "max-age=31536000", "Content-Security-Policy": "default-src 'self'", "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer"}
BAD = {"Server": "Apache/2.4.41", "X-Powered-By": "Express"}

def test_good(): r = analyze_headers(GOOD); assert r.grade in ("A", "B")
def test_missing(): r = analyze_headers({}); assert len(r.missing) > 0
def test_present(): r = analyze_headers(GOOD); assert len(r.present) >= 4
def test_server_info(): r = analyze_headers(BAD); assert any("Server" in i for i in r.issues)
def test_powered_by(): r = analyze_headers(BAD); assert any("Powered" in i for i in r.issues)
def test_xcto_ok(): r = analyze_headers({"X-Content-Type-Options": "nosniff"}); assert not any("X-Content-Type-Options" in i for i in r.issues)
def test_xcto_bad(): r = analyze_headers({"X-Content-Type-Options": "wrong"}); assert any("X-Content-Type-Options" in i for i in r.issues)
def test_xfo_deny(): r = analyze_headers({"X-Frame-Options": "DENY"}); assert not any("X-Frame-Options" in i for i in r.issues)
def test_xfo_bad(): r = analyze_headers({"X-Frame-Options": "ALLOW"}); assert any("X-Frame-Options" in i for i in r.issues)
def test_suggestions(): r = analyze_headers({}); assert len(r.suggestions) > 0
def test_score(): r = analyze_headers(GOOD); assert 0 <= r.score <= 100
def test_grade_bad(): r = analyze_headers(BAD); assert r.grade in ("D", "F")
def test_format(): md = format_result_markdown(analyze_headers(GOOD)); assert "Header Analysis" in md
def test_to_dict(): d = analyze_headers(GOOD).to_dict(); assert "score" in d
def test_count(): assert len(SECURITY_HEADERS) >= 6
