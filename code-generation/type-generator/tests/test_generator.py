"""Tests for Type Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import infer_json_type, infer_fields, generate_types

SAMPLE = {"id": 1, "name": "Alice", "email": "a@b.com", "active": True, "score": 3.14, "tags": ["admin", "user"], "address": {"city": "NYC", "zip": "10001"}, "orders": [{"id": 1, "total": 99.99}]}

def test_infer_string(): assert infer_json_type("hello") == "string"
def test_infer_number(): assert infer_json_type(42) == "number"
def test_infer_float(): assert infer_json_type(3.14) == "number"
def test_infer_bool(): assert infer_json_type(True) == "boolean"
def test_infer_null(): assert infer_json_type(None) == "null"
def test_infer_list(): assert infer_json_type([1,2]) == "array"
def test_infer_dict(): assert infer_json_type({}) == "object"

def test_infer_fields():
    fields = infer_fields(SAMPLE)
    names = [f.name for f in fields]
    assert "id" in names and "name" in names and "address" in names

def test_nested_fields():
    fields = infer_fields(SAMPLE)
    addr = next(f for f in fields if f.name == "address")
    assert len(addr.children) == 2

def test_array_items():
    fields = infer_fields(SAMPLE)
    tags = next(f for f in fields if f.name == "tags")
    assert tags.type_str == "string[]"

def test_object_array():
    fields = infer_fields(SAMPLE)
    orders = next(f for f in fields if f.name == "orders")
    assert orders.type_str == "object[]"

def test_typescript():
    ts = generate_types(SAMPLE, name="User", fmt="typescript")
    assert "interface User" in ts
    assert "id: number;" in ts
    assert "name: string;" in ts

def test_typescript_nested():
    ts = generate_types(SAMPLE, fmt="typescript")
    assert "city: string;" in ts

def test_python():
    py = generate_types(SAMPLE, name="User", fmt="python")
    assert "class User:" in py
    assert "id: float" in py
    assert "name: str" in py

def test_zod():
    zod = generate_types(SAMPLE, name="User", fmt="zod")
    assert "UserSchema" in zod
    assert "z.string()" in zod

def test_from_json_string():
    ts = generate_types('{"x": 1}', fmt="typescript")
    assert "x: number;" in ts

def test_from_array():
    ts = generate_types([{"a": 1}], fmt="typescript")
    assert "a: number;" in ts

def test_empty():
    ts = generate_types({}, fmt="typescript")
    assert "interface Root" in ts
