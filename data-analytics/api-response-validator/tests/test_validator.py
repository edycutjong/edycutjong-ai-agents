"""Tests for API Response Validator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.validator import validate_response, validate_type, create_rules_from_sample, format_result_markdown, ValidationRule

SAMPLE = {"id": 1, "name": "Alice", "email": "alice@test.com", "active": True, "tags": ["dev"]}

def test_valid_response():
    rules = create_rules_from_sample(SAMPLE)
    r = validate_response(SAMPLE, rules)
    assert r.is_valid

def test_missing_required():
    rules = [ValidationRule(field="name", required=True, expected_type="string")]
    r = validate_response({}, rules)
    assert not r.is_valid

def test_wrong_type():
    rules = [ValidationRule(field="age", expected_type="number")]
    r = validate_response({"age": "thirty"}, rules)
    assert not r.is_valid

def test_correct_type():
    rules = [ValidationRule(field="age", expected_type="number")]
    r = validate_response({"age": 30}, rules)
    assert r.is_valid

def test_type_string(): assert validate_type("hello", "string")
def test_type_number(): assert validate_type(42, "number")
def test_type_bool(): assert validate_type(True, "boolean")
def test_type_array(): assert validate_type([1, 2], "array")
def test_type_object(): assert validate_type({"a": 1}, "object")
def test_type_null(): assert validate_type(None, "null")

def test_min_length():
    rules = [ValidationRule(field="name", expected_type="string", min_length=5)]
    r = validate_response({"name": "ab"}, rules)
    assert not r.is_valid

def test_max_length():
    rules = [ValidationRule(field="name", expected_type="string", max_length=3)]
    r = validate_response({"name": "abcde"}, rules)
    assert not r.is_valid

def test_pattern():
    rules = [ValidationRule(field="email", expected_type="string", pattern=r"^[\w.]+@[\w.]+$")]
    r = validate_response({"email": "a@b.com"}, rules)
    assert r.is_valid

def test_pattern_fail():
    rules = [ValidationRule(field="email", expected_type="string", pattern=r"^[\w.]+@[\w.]+$")]
    r = validate_response({"email": "invalid"}, rules)
    assert not r.is_valid

def test_status_warning():
    rules = create_rules_from_sample(SAMPLE)
    r = validate_response(SAMPLE, rules, status_code=500)
    assert len(r.warnings) >= 1

def test_infer_rules():
    rules = create_rules_from_sample(SAMPLE)
    assert len(rules) == 5

def test_format():
    rules = create_rules_from_sample(SAMPLE)
    r = validate_response(SAMPLE, rules)
    md = format_result_markdown(r)
    assert "✅" in md

def test_create_rules_unsupported_type():
    rules = create_rules_from_sample({"location": (10.0, 20.0)})
    assert len(rules) == 1
    assert rules[0].field == "location"
    assert rules[0].expected_type == ""
