"""Tests for Password Strength Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import analyze_password, calculate_entropy, format_result_markdown, COMMON_PASSWORDS

def test_weak_password():
    r = analyze_password("123456")
    assert r.strength == "weak"

def test_strong_password():
    r = analyze_password("MyStr0ng!P@ssw0rd#2024")
    assert r.score >= 60

def test_length():
    r = analyze_password("abcdefgh")
    assert r.length == 8

def test_has_upper():
    r = analyze_password("Hello123!")
    assert r.has_upper

def test_has_lower():
    r = analyze_password("Hello123!")
    assert r.has_lower

def test_has_digit():
    r = analyze_password("Hello123!")
    assert r.has_digit

def test_has_special():
    r = analyze_password("Hello123!")
    assert r.has_special

def test_no_special():
    r = analyze_password("HelloWorld")
    assert not r.has_special

def test_common_detected():
    r = analyze_password("password")
    assert "Common password" in " ".join(r.issues)

def test_repeated_chars():
    r = analyze_password("aaaabbbb1111")
    assert any("Repeated" in i for i in r.issues)

def test_sequential():
    r = analyze_password("abc12345")
    assert any("Sequential" in i for i in r.issues)

def test_entropy_positive():
    e = calculate_entropy("Hello123!")
    assert e > 0

def test_entropy_increases():
    e1 = calculate_entropy("aaaa")
    e2 = calculate_entropy("Aa1!Bb2@Cc3#")
    assert e2 > e1

def test_suggestions_short():
    r = analyze_password("ab")
    assert any("12 characters" in s for s in r.suggestions)

def test_suggestions_no_upper():
    r = analyze_password("alllowercase123!")
    assert any("uppercase" in s for s in r.suggestions)

def test_score_capped():
    r = analyze_password("")
    assert 0 <= r.score <= 100

def test_to_dict():
    r = analyze_password("Test!123")
    d = r.to_dict()
    assert "score" in d and "strength" in d

def test_format():
    r = analyze_password("Hello123!World")
    md = format_result_markdown(r)
    assert "Password Analysis" in md

def test_common_db_size():
    assert len(COMMON_PASSWORDS) >= 20
