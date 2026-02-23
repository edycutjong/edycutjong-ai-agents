"""Tests for YAML-JSON Converter."""
import sys, os, pytest, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import json_to_yaml, yaml_to_json, convert_json_string_to_yaml, convert_yaml_string_to_json, detect_format

SAMPLE = {"name": "Alice", "age": 30, "active": True, "score": 3.14}

def test_json_to_yaml_string():
    yml = json_to_yaml({"name": "Alice"})
    assert "name: Alice" in yml

def test_json_to_yaml_number():
    yml = json_to_yaml({"age": 30})
    assert "age: 30" in yml

def test_json_to_yaml_bool():
    yml = json_to_yaml({"active": True})
    assert "active: true" in yml

def test_json_to_yaml_null():
    yml = json_to_yaml({"val": None})
    assert "val: null" in yml

def test_json_to_yaml_nested():
    yml = json_to_yaml({"user": {"name": "Bob"}})
    assert "user:" in yml and "name: Bob" in yml

def test_json_to_yaml_list():
    yml = json_to_yaml({"tags": ["a", "b"]})
    assert "- a" in yml and "- b" in yml

def test_yaml_to_json_string():
    d = yaml_to_json("name: Alice")
    assert d["name"] == "Alice"

def test_yaml_to_json_number():
    d = yaml_to_json("age: 30")
    assert d["age"] == 30

def test_yaml_to_json_bool():
    d = yaml_to_json("active: true")
    assert d["active"] == True

def test_yaml_to_json_null():
    d = yaml_to_json("val: null")
    assert d["val"] is None

def test_yaml_to_json_quoted():
    d = yaml_to_json('name: "Alice"')
    assert d["name"] == "Alice"

def test_roundtrip():
    yml = json_to_yaml(SAMPLE)
    back = yaml_to_json(yml)
    assert back["name"] == "Alice"
    assert back["age"] == 30

def test_convert_json_string():
    yml = convert_json_string_to_yaml('{"x": 1}')
    assert "x: 1" in yml

def test_convert_yaml_string():
    j = convert_yaml_string_to_json("x: 1")
    data = json.loads(j)
    assert data["x"] == 1

def test_detect_json():
    assert detect_format('{"a": 1}') == "json"

def test_detect_yaml():
    assert detect_format("a: 1") == "yaml"

def test_detect_array():
    assert detect_format('[1, 2]') == "json"

def test_special_chars():
    yml = json_to_yaml({"url": "https://example.com"})
    assert '"https://example.com"' in yml
