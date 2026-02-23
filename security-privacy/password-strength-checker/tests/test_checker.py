"""Tests for Password Strength Checker."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.checker import check_password, calculate_entropy, generate_policy_check, format_result_markdown, COMMON_PASSWORDS

def test_weak(): r = check_password("123"); assert r.strength == "weak"
def test_strong(): r = check_password("MyStr0ng!Pass#2025xx"); assert r.strength in ("good", "strong")
def test_length(): r = check_password("abcdefgh"); assert r.length == 8
def test_upper(): r = check_password("Abc"); assert r.has_upper
def test_lower(): r = check_password("abc"); assert r.has_lower
def test_digit(): r = check_password("abc1"); assert r.has_digit
def test_special(): r = check_password("abc!"); assert r.has_special
def test_no_special(): r = check_password("abcdef"); assert not r.has_special
def test_entropy(): e = calculate_entropy("Test1!ab"); assert e > 0
def test_entropy_empty(): assert calculate_entropy("") == 0
def test_common(): r = check_password("password"); assert any("Common" in i for i in r.issues)
def test_not_common(): r = check_password("xK9#mZ7!qR"); assert not any("Common" in i for i in r.issues)
def test_repeated(): r = check_password("aaa111bbb"); assert any("Repeated" in i for i in r.issues)
def test_short_issue(): r = check_password("ab"); assert any("short" in i for i in r.issues)
def test_policy_ok(): f = generate_policy_check("Test1!ab"); assert len(f) == 0
def test_policy_fail(): f = generate_policy_check("abc"); assert len(f) > 0
def test_score(): r = check_password("Str0ng!Pass#2025"); assert r.score >= 4
def test_format(): md = format_result_markdown(check_password("test")); assert "Password Check" in md
def test_to_dict(): d = check_password("test").to_dict(); assert "strength" in d
def test_masked(): r = check_password("secret"); assert "secret" not in r.password
