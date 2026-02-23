"""Tests for Regex Tester."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.tester import run_regex_test, validate_pattern, extract_groups, get_common_pattern, compile_pattern, format_result_markdown, COMMON_PATTERNS

def test_simple(): r = run_regex_test(r"\d+", "abc 123 def 456"); assert r.match_count == 2
def test_no_match(): r = run_regex_test(r"\d+", "no numbers here"); assert r.match_count == 0
def test_match_text(): r = run_regex_test(r"\w+", "hello"); assert r.matches[0].text == "hello"
def test_match_pos(): r = run_regex_test(r"world", "hello world"); assert r.matches[0].start == 6
def test_groups(): r = run_regex_test(r"(\d+)-(\d+)", "123-456"); assert r.matches[0].groups == ["123", "456"]
def test_case_flag(): r = run_regex_test(r"hello", "HELLO", flags="i"); assert r.match_count == 1
def test_multiline(): r = run_regex_test(r"^\w+", "line1\nline2", flags="m"); assert r.match_count == 2
def test_invalid(): r = run_regex_test(r"[invalid", "text"); assert not r.is_valid
def test_validate_ok(): ok, _ = validate_pattern(r"\d+"); assert ok
def test_validate_bad(): ok, err = validate_pattern(r"[bad"); assert not ok and err
def test_extract(): gs = extract_groups(r"(\w+)@(\w+)", "user@host"); assert gs[0]["groups"] == ["user", "host"]
def test_named(): gs = extract_groups(r"(?P<name>\w+)", "hello"); assert gs[0]["named"]["name"] == "hello"
def test_common_email(): p = get_common_pattern("email"); assert p and "+" not in p[:3]
def test_common_url(): assert get_common_pattern("url")
def test_common_missing(): assert get_common_pattern("nonexistent") == ""
def test_patterns_count(): assert len(COMMON_PATTERNS) >= 5
def test_format(): md = format_result_markdown(run_regex_test(r"\d", "a1b2")); assert "Regex Test" in md
def test_to_dict(): d = run_regex_test(r"\d", "1").to_dict(); assert "match_count" in d
