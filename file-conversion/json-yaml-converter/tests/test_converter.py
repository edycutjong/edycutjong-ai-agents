"""Tests for JSON/YAML/TOML Converter."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import (
    json_to_yaml, yaml_to_json, json_to_toml,
    validate_json, format_json, detect_format, convert,
)

SAMPLE_JSON = '{"name": "test", "version": 1, "active": true}'
NESTED_JSON = '{"server": {"host": "localhost", "port": 8080}, "debug": false}'

# --- JSON → YAML ---
def test_json_to_yaml():
    yaml = json_to_yaml(SAMPLE_JSON)
    assert "name: test" in yaml
    assert "version: 1" in yaml
    assert "active: true" in yaml

def test_json_to_yaml_nested():
    yaml = json_to_yaml(NESTED_JSON)
    assert "server:" in yaml
    assert "host: localhost" in yaml

# --- YAML → JSON ---
def test_yaml_to_json():
    yaml = "name: test\nversion: 1\nactive: true"
    result = json.loads(yaml_to_json(yaml))
    assert result["name"] == "test"
    assert result["version"] == 1

# --- JSON → TOML ---
def test_json_to_toml():
    toml = json_to_toml(SAMPLE_JSON)
    assert 'name = "test"' in toml
    assert "version = 1" in toml

def test_json_to_toml_nested():
    toml = json_to_toml(NESTED_JSON)
    assert "[server]" in toml
    assert 'host = "localhost"' in toml

def test_toml_rejects_non_dict():
    with pytest.raises(ValueError):
        json_to_toml("[1, 2, 3]")

# --- Validation ---
def test_validate_valid():
    r = validate_json(SAMPLE_JSON)
    assert r["valid"]
    assert r["type"] == "dict"

def test_validate_invalid():
    r = validate_json("{broken}")
    assert not r["valid"]
    assert "error" in r

def test_validate_array():
    r = validate_json("[1, 2, 3]")
    assert r["valid"]
    assert r["length"] == 3

# --- Formatting ---
def test_format_pretty():
    result = format_json('{"a":1,"b":2}', indent=4)
    assert "    " in result

def test_format_compact():
    result = format_json('{"a": 1, "b": 2}', compact=True)
    assert " " not in result

def test_format_sorted():
    result = format_json('{"b": 2, "a": 1}', sort_keys=True)
    assert result.index('"a"') < result.index('"b"')

# --- Detection ---
def test_detect_json_object():
    assert detect_format('{"key": "value"}') == "json"

def test_detect_json_array():
    assert detect_format('[1, 2, 3]') == "json"

def test_detect_yaml():
    assert detect_format("name: test\nversion: 1") == "yaml"

# --- Auto-Convert ---
def test_convert_json_to_yaml():
    result = convert(SAMPLE_JSON, "yaml")
    assert "name: test" in result

def test_convert_json_to_toml():
    result = convert(SAMPLE_JSON, "toml")
    assert 'name = "test"' in result

def test_convert_same_format():
    result = convert(SAMPLE_JSON, "json", source_format="json")
    assert result == SAMPLE_JSON

# --- Edge Cases ---
def test_empty_object():
    yaml = json_to_yaml('{}')
    assert yaml == "{}"

def test_empty_array():
    yaml = json_to_yaml('[]')
    assert yaml == "[]"

def test_null_values():
    yaml = json_to_yaml('{"key": null}')
    assert "null" in yaml

def test_boolean_values():
    yaml = json_to_yaml('{"a": true, "b": false}')
    assert "a: true" in yaml
    assert "b: false" in yaml
