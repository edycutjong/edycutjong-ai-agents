"""Tests for Config File Merger."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.merger import deep_merge, merge_configs, count_keys, diff_configs, format_result_markdown

A = {"name": "app", "port": 3000, "db": {"host": "localhost", "port": 5432}}
B = {"port": 8080, "db": {"port": 5433, "name": "prod"}, "debug": False}

def test_merge(): merged, _ = deep_merge(A, B); assert merged["port"] == 8080 and merged["name"] == "app"
def test_nested(): merged, _ = deep_merge(A, B); assert merged["db"]["host"] == "localhost" and merged["db"]["port"] == 5433
def test_new_keys(): merged, _ = deep_merge(A, B); assert "debug" in merged and merged["db"]["name"] == "prod"
def test_conflicts(): _, c = deep_merge(A, B); assert len(c) >= 1
def test_conflict_key(): _, c = deep_merge(A, B); assert "port" in [x.key for x in c]
def test_merge_configs(): r = merge_configs([A, B]); assert r.merged["port"] == 8080
def test_three(): r = merge_configs([A, B, {"debug": True, "version": "1.0"}]); assert r.merged["debug"] == True
def test_no_conflict(): r = merge_configs([{"a": 1}, {"b": 2}]); assert r.conflict_count == 0
def test_count(): assert count_keys({"a": 1, "b": {"c": 2}}) == 3
def test_diff_add(): d = diff_configs({"a": 1}, {"a": 1, "b": 2}); assert any("+ b" in x for x in d)
def test_diff_remove(): d = diff_configs({"a": 1, "b": 2}, {"a": 1}); assert any("- b" in x for x in d)
def test_diff_change(): d = diff_configs({"a": 1}, {"a": 2}); assert any("~ a" in x for x in d)
def test_empty(): r = merge_configs([]); assert r.total_keys == 0
def test_format_clean(): md = format_result_markdown(merge_configs([{"a": 1}, {"b": 2}])); assert "No conflicts" in md
def test_format_conflicts(): md = format_result_markdown(merge_configs([A, B])); assert "Conflicts" in md
def test_to_dict(): d = merge_configs([A, B]).to_dict(); assert "total_keys" in d
