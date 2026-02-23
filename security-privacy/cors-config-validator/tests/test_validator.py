"""Tests for CORS Config Validator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.validator import parse_cors_config, validate_cors, format_result_markdown, CorsConfig

def test_wildcard_origin():
    c = CorsConfig(allow_origins=["*"])
    r = validate_cors(c)
    assert r.score < 100 and any("Wildcard" in i for i in r.issues)

def test_wildcard_with_creds():
    c = CorsConfig(allow_origins=["*"], allow_credentials=True)
    r = validate_cors(c)
    assert r.risk_level in ("high", "critical")

def test_specific_origin():
    c = CorsConfig(allow_origins=["https://example.com"])
    r = validate_cors(c)
    assert r.score >= 80

def test_wildcard_methods():
    c = CorsConfig(allow_origins=["https://example.com"], allow_methods=["*"])
    r = validate_cors(c)
    assert any("methods" in i.lower() for i in r.issues)

def test_wildcard_headers():
    c = CorsConfig(allow_origins=["https://example.com"], allow_headers=["*"])
    r = validate_cors(c)
    assert r.score < 100

def test_dangerous_methods():
    c = CorsConfig(allow_origins=["https://example.com"], allow_methods=["GET", "DELETE"])
    r = validate_cors(c)
    assert any("DELETE" in s for s in r.suggestions)

def test_sensitive_header():
    c = CorsConfig(allow_origins=["https://example.com"], allow_headers=["authorization"])
    r = validate_cors(c)
    assert any("authorization" in s for s in r.suggestions)

def test_long_max_age():
    c = CorsConfig(allow_origins=["https://example.com"], max_age=172800)
    r = validate_cors(c)
    assert any("Max-age" in s for s in r.suggestions)

def test_parse_config():
    c = parse_cors_config({"allow_origins": ["*"], "allow_methods": "GET,POST", "allow_credentials": True})
    assert c.allow_origins == ["*"] and "GET" in c.allow_methods and c.allow_credentials

def test_parse_string_origin():
    c = parse_cors_config({"allow_origins": "https://example.com"})
    assert c.allow_origins == ["https://example.com"]

def test_parse_string_creds():
    c = parse_cors_config({"allow_credentials": "true"})
    assert c.allow_credentials == True

def test_secure_config():
    c = CorsConfig(allow_origins=["https://myapp.com"], allow_methods=["GET", "POST"], allow_credentials=True, max_age=3600)
    r = validate_cors(c)
    assert r.risk_level == "low"

def test_score_capped():
    c = CorsConfig(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)
    r = validate_cors(c)
    assert r.score >= 0

def test_format():
    c = CorsConfig(allow_origins=["*"])
    r = validate_cors(c)
    md = format_result_markdown(c, r)
    assert "CORS Validation" in md

def test_to_dict():
    c = CorsConfig(allow_origins=["*"])
    r = validate_cors(c)
    d = r.to_dict()
    assert "score" in d
