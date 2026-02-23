"""Tests for Env File Auditor."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.auditor import parse_env, audit_env, compare_envs, generate_env_template, format_audit_markdown

SAMPLE = """
DATABASE_URL=postgres://localhost/mydb
API_KEY=abc123secret
SECRET_KEY=mysupersecret
DEBUG=true
PORT=3000
"""

def test_parse():
    entries = parse_env(SAMPLE)
    assert len(entries) == 5
    keys = [e.key for e in entries]
    assert "DATABASE_URL" in keys

def test_parse_skip_comments():
    entries = parse_env("# comment\nKEY=val")
    assert len(entries) == 1

def test_parse_empty_value():
    entries = parse_env("KEY=")
    assert entries[0].has_value == False

def test_sensitive_detection():
    entries = parse_env(SAMPLE)
    sensitive = [e for e in entries if e.is_sensitive]
    assert len(sensitive) >= 2  # API_KEY, SECRET_KEY

def test_audit_clean():
    r = audit_env("DEBUG=true\nPORT=3000")
    assert r.score == 100
    assert len(r.issues) == 0

def test_audit_missing_value():
    r = audit_env("API_KEY=\nDEBUG=true")
    assert "API_KEY" in r.missing_values

def test_audit_sensitive_exposed():
    r = audit_env("SECRET_KEY=mysupersecret")
    assert "SECRET_KEY" in r.sensitive_exposed

def test_audit_duplicate():
    r = audit_env("KEY=a\nKEY=b")
    assert "KEY" in r.duplicates

def test_audit_score_deduction():
    r = audit_env("SECRET_KEY=exposed\nAPI_KEY=")
    assert r.score < 100

def test_compare_same():
    r = compare_envs("A=1\nB=2", "A=1\nB=2")
    assert len(r.only_in_a) == 0 and len(r.only_in_b) == 0

def test_compare_diff():
    r = compare_envs("A=1\nB=2", "A=1\nC=3")
    assert "B" in r.only_in_a
    assert "C" in r.only_in_b

def test_compare_diff_values():
    r = compare_envs("A=1", "A=2")
    assert "A" in r.different_values

def test_template_strips_secrets():
    tmpl = generate_env_template("SECRET_KEY=mysupersecret\nDEBUG=true")
    assert "mysupersecret" not in tmpl
    assert "SECRET_KEY=" in tmpl

def test_template_keeps_nonsecret():
    tmpl = generate_env_template("DEBUG=true")
    assert "DEBUG=true" in tmpl

def test_format_clean():
    r = audit_env("DEBUG=true")
    md = format_audit_markdown(r)
    assert "✅" in md

def test_format_issues():
    r = audit_env("SECRET_KEY=exposed")
    md = format_audit_markdown(r)
    assert "Issues" in md

def test_to_dict():
    r = audit_env(SAMPLE)
    d = r.to_dict()
    assert "score" in d and "total" in d
