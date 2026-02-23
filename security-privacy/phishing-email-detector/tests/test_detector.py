"""Tests for Phishing Email Detector."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.detector import analyze_email, format_result_markdown, SUSPICIOUS_PHRASES

LEGIT_EMAIL = "Hi team, the quarterly report is ready for review. Please see the attached PDF."
PHISH_EMAIL = "Dear customer, your account has been compromised! Click here immediately to verify your account: https://bit.ly/fake-login. Enter your password and credit card to confirm."

def test_legit_low_risk():
    r = analyze_email("Quarterly Report", LEGIT_EMAIL)
    assert r.risk_level == "low"

def test_phish_high_risk():
    r = analyze_email("URGENT ACTION REQUIRED", PHISH_EMAIL, sender="support12345@fake.xyz")
    assert r.risk_score >= 45

def test_suspicious_phrases():
    r = analyze_email("Alert", "verify your account now")
    assert len(r.suspicious_phrases_found) >= 1

def test_urgency_detection():
    r = analyze_email("", "act now before it expires immediately")
    assert r.has_urgency

def test_url_detection():
    r = analyze_email("", "click https://example.com/login")
    assert len(r.urls_found) == 1

def test_suspicious_url():
    r = analyze_email("", "click https://bit.ly/sus-link")
    assert r.has_suspicious_links

def test_pii_request():
    r = analyze_email("", "please send your password and credit card")
    assert r.has_personal_info_request

def test_sender_numbers():
    r = analyze_email("Hi", "hello", sender="user123456@spam.com")
    assert any("numbers" in i for i in r.indicators)

def test_caps_abuse():
    r = analyze_email("FREE MONEY NOW WIN BIG", "some body text")
    assert any("capitalization" in i for i in r.indicators)

def test_clean_email():
    r = analyze_email("Meeting Tomorrow", "Let's meet at 2pm to discuss the project.")
    assert r.risk_score < 20

def test_score_capped():
    r = analyze_email("URGENT", PHISH_EMAIL, sender="x@y")
    assert r.risk_score <= 100

def test_risk_levels():
    r1 = analyze_email("Hi", "normal email")
    assert r1.risk_level == "low"

def test_to_dict():
    r = analyze_email("test", "test body")
    d = r.to_dict()
    assert "risk_score" in d and "risk_level" in d

def test_format_clean():
    r = analyze_email("Hi", "normal")
    md = format_result_markdown(r)
    assert "✅" in md

def test_format_risky():
    r = analyze_email("URGENT", PHISH_EMAIL)
    md = format_result_markdown(r)
    assert "Indicators" in md

def test_phrases_count():
    assert len(SUSPICIOUS_PHRASES) >= 15
