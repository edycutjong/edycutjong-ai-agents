"""Tests for JSON Formatter."""
import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.formatter import format_json, extract_paths, get_value, sort_keys_recursive, format_result_markdown

SIMPLE = '{"name":"Alice","age":30}'
NESTED = '{"user":{"name":"Alice","address":{"city":"NYC"}}}'
ARRAY = '[1,2,3]'
INVALID = '{"unclosed":'

def test_valid(): r = format_json(SIMPLE); assert r.is_valid
def test_formatted(): r = format_json(SIMPLE); assert '"name"' in r.formatted
def test_minified(): r = format_json(SIMPLE); assert " " not in r.minified
def test_invalid(): r = format_json(INVALID); assert not r.is_valid and r.error
def test_key_count(): r = format_json(SIMPLE); assert r.key_count == 2
def test_nested_keys(): r = format_json(NESTED); assert r.key_count >= 3
def test_depth(): r = format_json(NESTED); assert r.depth >= 2
def test_sort(): r = format_json(SIMPLE, sort_keys=True); keys = list(json.loads(r.formatted).keys()); assert keys == sorted(keys)
def test_indent(): r = format_json(SIMPLE, indent=4); assert "    " in r.formatted
def test_size(): r = format_json(SIMPLE); assert r.size_bytes > 0
def test_paths(): paths = extract_paths(SIMPLE); assert "$.name" in paths
def test_array_paths(): paths = extract_paths(ARRAY); assert "$.length" not in paths
def test_get_value(): assert get_value(SIMPLE, "name") == "Alice"
def test_get_missing(): assert get_value(SIMPLE, "missing") == ""
def test_sort_recursive(): s = sort_keys_recursive('{"b":1,"a":2}'); assert list(json.loads(s).keys()) == ["a", "b"]
def test_format(): md = format_result_markdown(format_json(SIMPLE)); assert "JSON Formatter" in md
def test_to_dict(): d = format_json(SIMPLE).to_dict(); assert "key_count" in d
