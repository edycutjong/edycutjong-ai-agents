"""Tests for Env Validator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.validator import parse_env, check_required, redact_sensitive, to_dict, compare_envs, format_result_markdown

ENV = "DB_HOST=localhost\nDB_PORT=5432\nAPI_KEY=secret123\n"
EMPTY_VAL = "FOO=\nBAR=hello\n"
QUOTED = 'NAME="John Doe"\nPATH_VAL=/usr/bin\n'
COMMENT = "# comment\nFOO=bar\n"
INVALID_KEY = "foo_bar=value\n"
NO_EQUALS = "INVALID_LINE\n"

def test_parse(): r = parse_env(ENV); assert r.count == 3
def test_key(): r = parse_env(ENV); assert r.variables[0].key == "DB_HOST"
def test_value(): r = parse_env(ENV); assert r.variables[0].value == "localhost"
def test_empty_value(): r = parse_env(EMPTY_VAL); assert r.empty_count == 1
def test_quoted(): r = parse_env(QUOTED); assert r.variables[0].value == "John Doe"
def test_comment_skip(): r = parse_env(COMMENT); assert r.count == 1
def test_invalid_key(): r = parse_env(INVALID_KEY); assert len(r.issues) >= 1
def test_no_equals(): r = parse_env(NO_EQUALS); assert not r.is_valid
def test_required_ok(): r = parse_env(ENV); m = check_required(r, ["DB_HOST"]); assert m == []
def test_required_missing(): r = parse_env(ENV); m = check_required(r, ["MISSING_KEY"]); assert "MISSING_KEY" in m
def test_redact(): r = parse_env(ENV); d = redact_sensitive(r); assert d.get("API_KEY") == "***REDACTED***"
def test_no_redact(): r = parse_env(ENV); d = redact_sensitive(r); assert d.get("DB_HOST") == "localhost"
def test_to_dict(): r = parse_env(ENV); d = to_dict(r); assert d.get("DB_HOST") == "localhost"
def test_compare(): r1 = parse_env("A=1\nB=2\n"); r2 = parse_env("B=2\nC=3\n"); diff = compare_envs(r1, r2); assert "A" in diff["only_in_first"]
def test_format(): md = format_result_markdown(parse_env(ENV)); assert "Env Validator" in md
def test_to_dict_result(): d = parse_env(ENV).to_dict(); assert "count" in d
