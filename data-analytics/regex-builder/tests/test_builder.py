"""Tests for Regex Builder."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.builder import run_test, get_pattern, list_patterns, explain_pattern, validate_pattern, build_pattern, format_test_markdown, COMMON_PATTERNS

def test_email_pattern():
    r = run_test(get_pattern("email"), "contact me at alice@example.com today")
    assert r.match_count == 1 and "alice@example.com" in r.matches

def test_url_pattern():
    r = run_test(get_pattern("url"), "visit https://example.com now")
    assert r.match_count == 1

def test_ipv4_pattern():
    r = run_test(get_pattern("ipv4"), "server at 192.168.1.1")
    assert "192.168.1.1" in r.matches

def test_date_iso():
    r = run_test(get_pattern("date_iso"), "born 2024-01-15")
    assert "2024-01-15" in r.matches

def test_hex_color():
    r = run_test(get_pattern("hex_color"), "color: #ff0000")
    assert "#ff0000" in r.matches

def test_semver():
    r = run_test(get_pattern("semver"), "version v1.2.3-beta")
    assert r.match_count == 1

def test_no_match():
    r = run_test(r"\d+", "no numbers here")
    assert r.match_count == 0

def test_invalid_pattern():
    r = run_test("[invalid", "test")
    assert r.is_valid == False and r.error

def test_get_pattern():
    assert get_pattern("email") is not None

def test_get_unknown():
    assert get_pattern("nonexistent") is None

def test_list_patterns():
    patterns = list_patterns()
    assert len(patterns) >= 10
    assert "email" in patterns

def test_explain():
    exp = explain_pattern(r"\d+@\w+")
    assert "digit" in exp

def test_validate_valid():
    ok, msg = validate_pattern(r"\d+")
    assert ok

def test_validate_invalid():
    ok, msg = validate_pattern("[bad")
    assert not ok

def test_build():
    p = build_pattern(["email"])
    assert "@" in p

def test_format_matches():
    r = run_test(r"\d+", "a1b2c3")
    md = format_test_markdown(r)
    assert "3 matches" in md

def test_format_no_match():
    r = run_test(r"\d+", "abc")
    md = format_test_markdown(r)
    assert "No matches" in md

def test_common_count():
    assert len(COMMON_PATTERNS) >= 14
