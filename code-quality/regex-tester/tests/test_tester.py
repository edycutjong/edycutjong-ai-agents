"""Tests for Regex Tester."""
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.tester import (
    run_regex_test, validate_pattern, batch_test, explain_pattern,
    format_result_markdown, COMMON_PATTERNS, parse_flags,
)


# --- Pattern Testing ---

def test_simple_match():
    """Finds simple matches."""
    result = run_regex_test(r"\d+", "abc 123 def 456")
    assert result.is_valid
    assert result.match_count == 2
    assert result.matches[0].match == "123"
    assert result.matches[1].match == "456"


def test_no_match():
    """Returns 0 matches when nothing matches."""
    result = run_regex_test(r"\d+", "no numbers here")
    assert result.is_valid
    assert result.match_count == 0


def test_invalid_pattern():
    """Reports invalid regex."""
    result = run_regex_test(r"[unclosed", "test")
    assert not result.is_valid
    assert result.error != ""


def test_groups():
    """Captures named and unnamed groups."""
    result = run_regex_test(r"(\w+)@(\w+)\.(\w+)", "user@example.com")
    assert result.match_count == 1
    assert result.matches[0].groups == ("user", "example", "com")


def test_named_groups():
    """Captures named groups."""
    result = run_regex_test(r"(?P<name>\w+)@(?P<domain>\w+\.\w+)", "user@example.com")
    assert result.matches[0].group_dict["name"] == "user"
    assert result.matches[0].group_dict["domain"] == "example.com"


def test_flags_ignorecase():
    """Case-insensitive flag works."""
    result = run_regex_test(r"hello", "Hello World HELLO", flags="i")
    assert result.match_count == 2


def test_flags_multiline():
    """Multiline flag works with ^ and $."""
    result = run_regex_test(r"^\w+", "first\nsecond\nthird", flags="m")
    assert result.match_count == 3


def test_match_positions():
    """Match positions are correct."""
    result = run_regex_test(r"\w+", "abc def")
    assert result.matches[0].start == 0
    assert result.matches[0].end == 3
    assert result.matches[1].start == 4


# --- Validation ---

def test_validate_valid():
    """Valid pattern returns valid=True."""
    info = validate_pattern(r"\d{3}-\d{4}")
    assert info["valid"]
    assert info["groups"] == 0


def test_validate_with_groups():
    """Validation reports group count and names."""
    info = validate_pattern(r"(?P<area>\d{3})-(?P<num>\d{4})")
    assert info["valid"]
    assert info["groups"] == 2
    assert "area" in info["group_names"]


def test_validate_invalid():
    """Invalid pattern reports error."""
    info = validate_pattern(r"(unclosed")
    assert not info["valid"]
    assert "error" in info


# --- Batch Testing ---

def test_batch_test():
    """Tests multiple patterns at once."""
    results = batch_test([r"\d+", r"[a-z]+", r"NOPE"], "abc 123")
    assert len(results) == 3
    assert results[0].match_count == 1  # \d+
    assert results[1].match_count == 1  # [a-z]+
    assert results[2].match_count == 0  # NOPE


# --- Common Patterns Library ---

def test_common_email():
    """Email pattern matches valid email."""
    result = run_regex_test(COMMON_PATTERNS["email"], "Contact user@example.com please")
    assert result.match_count == 1
    assert result.matches[0].match == "user@example.com"


def test_common_url():
    """URL pattern matches URLs."""
    result = run_regex_test(COMMON_PATTERNS["url"], "Visit https://example.com/page today")
    assert result.match_count == 1


def test_common_ipv4():
    """IPv4 pattern matches IPs."""
    result = run_regex_test(COMMON_PATTERNS["ipv4"], "Server at 192.168.1.1 and 10.0.0.1")
    assert result.match_count == 2


def test_common_date_iso():
    """ISO date pattern matches."""
    result = run_regex_test(COMMON_PATTERNS["date_iso"], "Born on 2023-04-15")
    assert result.match_count == 1


def test_common_uuid():
    """UUID pattern matches."""
    result = run_regex_test(COMMON_PATTERNS["uuid"], "ID: 550e8400-e29b-41d4-a716-446655440000")
    assert result.match_count == 1


def test_common_patterns_all_valid():
    """All common patterns are valid regex."""
    for name, pattern in COMMON_PATTERNS.items():
        info = validate_pattern(pattern)
        assert info["valid"], f"Pattern '{name}' is invalid: {info.get('error')}"


# --- Explanation ---

def test_explain_pattern():
    """Explain returns component descriptions."""
    parts = explain_pattern(r"\d+")
    assert len(parts) >= 2
    assert any("digit" in p for p in parts)


# --- Markdown Output ---

def test_format_markdown():
    """Markdown output contains expected sections."""
    result = run_regex_test(r"\d+", "abc 123 def 456")
    md = format_result_markdown(result)
    assert "# Regex Test" in md
    assert "✅" in md
    assert "123" in md


def test_format_markdown_invalid():
    """Markdown shows error for invalid pattern."""
    result = run_regex_test(r"[bad", "test")
    md = format_result_markdown(result)
    assert "❌" in md


# --- Parse Flags ---

def test_parse_flags():
    """Flag parsing converts string to re flags."""
    import re
    flags = parse_flags("im")
    assert flags & re.IGNORECASE
    assert flags & re.MULTILINE
