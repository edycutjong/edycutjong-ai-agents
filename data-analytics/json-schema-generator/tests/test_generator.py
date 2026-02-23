"""Tests for JSON Schema Generator."""
import sys, os, pytest, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import infer_type, infer_string_format, generate_schema, generate_from_json, validate_against_schema, format_schema

SAMPLE = {"id": 1, "name": "Alice", "email": "a@b.com", "active": True, "score": 3.14, "tags": ["admin"], "address": {"city": "NYC"}, "created": "2024-01-15"}

def test_infer_string(): assert infer_type("hi") == "string"
def test_infer_integer(): assert infer_type(42) == "integer"
def test_infer_float(): assert infer_type(3.14) == "number"
def test_infer_bool(): assert infer_type(True) == "boolean"
def test_infer_null(): assert infer_type(None) == "null"
def test_infer_list(): assert infer_type([]) == "array"
def test_infer_dict(): assert infer_type({}) == "object"

def test_format_email(): assert infer_string_format("a@b.com") == "email"
def test_format_uri(): assert infer_string_format("https://a.com") == "uri"
def test_format_date(): assert infer_string_format("2024-01-15") == "date"
def test_format_datetime(): assert infer_string_format("2024-01-15T10:00:00Z") == "date-time"
def test_format_none(): assert infer_string_format("hello") is None

def test_schema_object():
    s = generate_schema(SAMPLE)
    assert s["type"] == "object"
    assert "name" in s["properties"]

def test_schema_required():
    s = generate_schema(SAMPLE)
    assert "name" in s["required"]

def test_schema_nested():
    s = generate_schema(SAMPLE)
    assert s["properties"]["address"]["type"] == "object"

def test_schema_array():
    s = generate_schema(SAMPLE)
    assert s["properties"]["tags"]["type"] == "array"

def test_schema_format():
    s = generate_schema(SAMPLE)
    assert s["properties"]["email"].get("format") == "email"

def test_from_json():
    s = generate_from_json(json.dumps(SAMPLE))
    assert s["type"] == "object"

def test_from_array():
    s = generate_from_json(json.dumps([SAMPLE]))
    assert s["type"] == "object"

def test_validate_ok():
    s = generate_schema(SAMPLE)
    errors = validate_against_schema(SAMPLE, s)
    assert len(errors) == 0

def test_validate_missing():
    s = generate_schema(SAMPLE)
    errors = validate_against_schema({"id": 1}, s)
    assert any("Missing" in e for e in errors)

def test_validate_type_mismatch():
    s = generate_schema({"age": 25})
    errors = validate_against_schema({"age": "old"}, s)
    assert any("mismatch" in e for e in errors)

def test_format_output():
    s = generate_schema({"x": 1})
    out = format_schema(s)
    assert '"type"' in out

def test_title():
    s = generate_schema({"x": 1}, title="MySchema")
    assert s["title"] == "MySchema"

def test_empty_array():
    s = generate_schema({"items": []})
    assert s["properties"]["items"]["type"] == "array"
