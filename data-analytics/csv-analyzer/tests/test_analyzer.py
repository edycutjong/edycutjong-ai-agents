"""Tests for CSV Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import analyze_csv, profile_column, detect_type, get_column_stats, format_result_markdown

CSV = "name,age,city\nAlice,30,NYC\nBob,25,LA\nCharlie,35,NYC\n"
CSV_NULLS = "name,age\nAlice,30\nBob,\nCharlie,25\n"

def test_rows(): r = analyze_csv(CSV); assert r.rows == 3
def test_columns(): r = analyze_csv(CSV); assert r.columns == 3
def test_col_names(): r = analyze_csv(CSV); assert r.column_names == ["name", "age", "city"]
def test_profile_count(): r = analyze_csv(CSV); assert len(r.profiles) == 3
def test_numeric(): assert detect_type(["1", "2", "3"]) == "numeric"
def test_string(): assert detect_type(["a", "b", "c"]) == "string"
def test_profile_unique(): p = profile_column("city", ["NYC", "LA", "NYC"]); assert p.unique == 2
def test_profile_nulls(): p = profile_column("age", ["30", "", "25"]); assert p.nulls == 1
def test_numeric_stats(): p = profile_column("age", ["30", "25", "35"]); assert p.mean == 30.0
def test_min_max(): p = profile_column("age", ["30", "25", "35"]); assert p.min_val == "25.0" and p.max_val == "35.0"
def test_top_values(): p = profile_column("city", ["NYC", "LA", "NYC"]); assert "NYC" in p.top_values
def test_empty(): r = analyze_csv(""); assert r.rows == 0
def test_col_stats(): s = get_column_stats(CSV, "age"); assert s.get("type") == "numeric"
def test_col_missing(): s = get_column_stats(CSV, "nonexistent"); assert s == {}
def test_nulls_csv(): r = analyze_csv(CSV_NULLS); assert r.profiles[1].nulls == 1
def test_format(): md = format_result_markdown(analyze_csv(CSV)); assert "CSV Analysis" in md
def test_to_dict(): d = analyze_csv(CSV).to_dict(); assert "rows" in d
