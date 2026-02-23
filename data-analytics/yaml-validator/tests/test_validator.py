"""Tests for YAML Validator."""
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.validator import validate_yaml, yaml_to_json, get_keys, format_result_markdown

SIMPLE = "name: Alice\nage: 30\n"
NESTED = "server:\n  host: localhost\n  port: 8080\n"
TYPES = "active: true\ncount: 42\npi: 3.14\nlabel: hello\n"
COMMENT = "# comment\nkey: value\n"

def test_valid(): r = validate_yaml(SIMPLE); assert r.is_valid
def test_keys(): r = validate_yaml(SIMPLE); assert r.key_count == 2
def test_lines(): r = validate_yaml(SIMPLE); assert r.line_count >= 2
def test_nested(): r = validate_yaml(NESTED); assert r.key_count >= 3
def test_nested_val(): r = validate_yaml(NESTED); assert r.data["server"]["host"] == "localhost"
def test_bool(): r = validate_yaml(TYPES); assert r.data["active"] is True
def test_int(): r = validate_yaml(TYPES); assert r.data["count"] == 42
def test_float(): r = validate_yaml(TYPES); assert abs(r.data["pi"] - 3.14) < 0.01
def test_string(): r = validate_yaml(TYPES); assert r.data["label"] == "hello"
def test_comment(): r = validate_yaml(COMMENT); assert r.key_count == 1
def test_to_json(): j = yaml_to_json(SIMPLE); d = json.loads(j); assert d["name"] == "Alice"
def test_get_keys(): keys = get_keys(SIMPLE); assert "name" in keys
def test_nested_keys(): keys = get_keys(NESTED); assert any("host" in k for k in keys)
def test_empty(): r = validate_yaml(""); assert r.is_valid
def test_format(): md = format_result_markdown(validate_yaml(SIMPLE)); assert "YAML Validator" in md
def test_to_dict(): d = validate_yaml(SIMPLE).to_dict(); assert "is_valid" in d
