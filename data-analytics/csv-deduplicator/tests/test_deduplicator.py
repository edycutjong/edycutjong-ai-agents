"""Tests for CSV Deduplicator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.deduplicator import parse_csv, deduplicate, find_duplicates, to_csv_string, row_hash, format_result_markdown

CSV_DATA = """name,email,age
Alice,alice@example.com,30
Bob,bob@example.com,25
Alice,alice@example.com,30
Charlie,charlie@example.com,35
Bob,bob@example.com,25"""

def test_parse_csv():
    headers, rows = parse_csv(CSV_DATA)
    assert headers == ["name", "email", "age"]
    assert len(rows) == 5

def test_deduplicate():
    headers, rows = parse_csv(CSV_DATA)
    unique, result = deduplicate(headers, rows)
    assert result.unique_rows == 3

def test_duplicates_removed():
    headers, rows = parse_csv(CSV_DATA)
    _, result = deduplicate(headers, rows)
    assert result.duplicates_removed == 2

def test_duplicate_groups():
    headers, rows = parse_csv(CSV_DATA)
    _, result = deduplicate(headers, rows)
    assert result.duplicate_groups == 2

def test_no_duplicates():
    csv = "a,b\n1,2\n3,4"
    headers, rows = parse_csv(csv)
    _, result = deduplicate(headers, rows)
    assert result.duplicates_removed == 0

def test_key_columns():
    csv = "name,email,age\nAlice,a@b.com,30\nAlice,a@b.com,31"
    headers, rows = parse_csv(csv)
    _, result = deduplicate(headers, rows, key_columns=[0, 1])
    assert result.unique_rows == 1

def test_find_duplicates():
    headers, rows = parse_csv(CSV_DATA)
    groups = find_duplicates(headers, rows)
    assert len(groups) == 2

def test_row_hash():
    h1 = row_hash(["a", "b"])
    h2 = row_hash(["a", "b"])
    h3 = row_hash(["a", "c"])
    assert h1 == h2 and h1 != h3

def test_hash_column_specific():
    h1 = row_hash(["a", "b", "c"], columns=[0])
    h2 = row_hash(["a", "x", "y"], columns=[0])
    assert h1 == h2

def test_to_csv_string():
    s = to_csv_string(["a", "b"], [["1", "2"], ["3", "4"]])
    assert "a,b" in s and "1,2" in s

def test_roundtrip():
    headers, rows = parse_csv(CSV_DATA)
    unique, _ = deduplicate(headers, rows)
    csv_out = to_csv_string(headers, unique)
    h2, r2 = parse_csv(csv_out)
    assert h2 == headers and len(r2) == 3

def test_format_clean():
    headers, rows = parse_csv("a,b\n1,2")
    _, result = deduplicate(headers, rows)
    md = format_result_markdown(result)
    assert "No duplicates" in md

def test_format_dupes():
    headers, rows = parse_csv(CSV_DATA)
    _, result = deduplicate(headers, rows)
    md = format_result_markdown(result)
    assert "Removed" in md

def test_to_dict():
    headers, rows = parse_csv(CSV_DATA)
    _, result = deduplicate(headers, rows)
    d = result.to_dict()
    assert d["duplicates_removed"] == 2

def test_empty():
    headers, rows = parse_csv("")
    assert headers == [] and rows == []
