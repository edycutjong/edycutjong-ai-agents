"""Comprehensive tests for CSV Cleaner."""
import sys
import os
import io
import tempfile
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.cleaner import CSVCleaner, CleaningReport


# --- Fixtures ---

MESSY_CSV = """name,age,email,date_joined
  Alice ,30, alice@test.com ,2023-01-15
Bob,25,bob@test.com,Jan 20 2023
  Alice ,30, alice@test.com ,2023-01-15
Charlie,,charlie@test.com,2023/02/01
David,abc,david@test.com,2023-03-10
"""

CLEAN_CSV = """name,age,email
Alice,30,alice@test.com
Bob,25,bob@test.com
Charlie,35,charlie@test.com
"""


# --- Encoding Tests ---

def test_detect_utf8_encoding():
    """Detects UTF-8 encoding."""
    cleaner = CSVCleaner()
    enc = cleaner.detect_encoding(b"hello,world\nalice,30")
    assert enc.lower() in ("utf-8", "ascii")


def test_load_from_content():
    """Load CSV from string content."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=CLEAN_CSV)
    assert len(df) == 3
    assert list(df.columns) == ["name", "age", "email"]


def test_load_from_bytes():
    """Load CSV from raw bytes."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(raw_bytes=CLEAN_CSV.encode("utf-8"))
    assert len(df) == 3


# --- Whitespace Tests ---

def test_trim_whitespace():
    """Strips leading/trailing whitespace from cells."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=MESSY_CSV)
    df = cleaner.trim_whitespace(df)
    assert df.iloc[0]["name"] == "Alice"
    assert df.iloc[0]["email"] == "alice@test.com"
    assert cleaner.report.whitespace_trimmed > 0


def test_trim_column_names():
    """Strips whitespace from column headers."""
    cleaner = CSVCleaner()
    csv_data = "  name  , age ,email\nAlice,30,a@b.com"
    df = cleaner.load_csv(content=csv_data)
    df = cleaner.trim_whitespace(df)
    assert "name" in df.columns
    assert "age" in df.columns


# --- Duplicate Tests ---

def test_remove_duplicates():
    """Removes exact duplicate rows."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=MESSY_CSV)
    df = cleaner.trim_whitespace(df)  # needed so duplicates match
    original = len(df)
    df = cleaner.remove_duplicates(df)
    assert len(df) < original
    assert cleaner.report.duplicates_removed > 0


def test_no_duplicates():
    """No-op when no duplicates exist."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=CLEAN_CSV)
    df = cleaner.remove_duplicates(df)
    assert cleaner.report.duplicates_removed == 0


# --- Missing Values Tests ---

def test_handle_missing_drop():
    """Drop strategy removes rows with missing values."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=MESSY_CSV)
    before = len(df)
    df = cleaner.handle_missing_values(df, strategy="drop")
    assert len(df) < before


def test_handle_missing_fill_empty():
    """Fill_empty replaces NaN with empty string."""
    cleaner = CSVCleaner()
    csv_data = "name,age\nAlice,30\nBob,\n"
    df = cleaner.load_csv(content=csv_data)
    df = cleaner.handle_missing_values(df, strategy="fill_empty")
    assert df.iloc[1]["age"] == ""
    assert not df.isnull().any().any()


def test_handle_missing_fill_mean():
    """Fill_mean fills numeric columns with mean."""
    cleaner = CSVCleaner()
    csv_data = "name,score\nAlice,80\nBob,\nCharlie,100\n"
    df = cleaner.load_csv(content=csv_data)
    df = cleaner.handle_missing_values(df, strategy="fill_mean")
    # Bob's score should be mean of 80 and 100 = 90
    assert df.iloc[1]["score"] == 90.0


def test_no_missing_values():
    """No-op when no missing values exist."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=CLEAN_CSV)
    df = cleaner.handle_missing_values(df, strategy="drop")
    assert cleaner.report.missing_values_filled == 0


# --- Date Standardization Tests ---

def test_standardize_dates():
    """Converts various date formats to YYYY-MM-DD."""
    cleaner = CSVCleaner()
    csv_data = "name,joined\nAlice,Jan 15 2023\nBob,2023/02/20\nCharlie,03-10-2023\n"
    df = cleaner.load_csv(content=csv_data)
    df = cleaner.standardize_dates(df, columns=["joined"])
    assert df.iloc[0]["joined"] == "2023-01-15"
    assert df.iloc[1]["joined"] == "2023-02-20"
    assert cleaner.report.date_standardized == 1


# --- Type Fixing Tests ---

def test_fix_numeric_types():
    """Converts string numbers to numeric type."""
    cleaner = CSVCleaner()
    csv_data = "name,score\nAlice,90\nBob,85\n"
    df = cleaner.load_csv(content=csv_data)
    assert df["score"].dtype == object or df["score"].dtype == "int64"
    df = cleaner.fix_column_types(df)
    assert pd.api.types.is_numeric_dtype(df["score"])


# --- Full Pipeline Tests ---

def test_full_clean_pipeline():
    """Full cleaning pipeline processes messy CSV."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=MESSY_CSV)
    df = cleaner.clean(df, missing_strategy="drop")

    assert cleaner.report.original_rows > cleaner.report.final_rows
    assert len(cleaner.report.actions) > 0


def test_clean_already_clean():
    """Clean pipeline on already-clean data is a no-op except reporting."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=CLEAN_CSV)
    df = cleaner.clean(df)
    assert cleaner.report.final_rows == 3


# --- Report Tests ---

def test_report_to_dict():
    """Report serializes to dict."""
    report = CleaningReport(original_rows=100, final_rows=90, original_columns=5)
    d = report.to_dict()
    assert d["original_rows"] == 100
    assert d["rows_removed"] == 10


def test_report_to_markdown():
    """Report generates readable Markdown."""
    report = CleaningReport(original_rows=100, final_rows=90, original_columns=5)
    report.actions = ["Removed 10 duplicate rows", "Trimmed whitespace"]
    md = report.to_markdown()
    assert "# CSV Cleaning Report" in md
    assert "Removed 10 duplicate rows" in md


# --- Quality Summary Tests ---

def test_quality_summary():
    """Quality summary reports correct stats."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=CLEAN_CSV)
    summary = cleaner.get_quality_summary(df)
    assert summary["rows"] == 3
    assert summary["columns"] == 3
    assert summary["missing_cells"] == 0
    assert summary["duplicate_rows"] == 0


# --- Save/Load Tests ---

def test_save_and_load_roundtrip():
    """Save cleaned CSV and reload it."""
    cleaner = CSVCleaner()
    df = cleaner.load_csv(content=CLEAN_CSV)

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        path = f.name

    try:
        cleaner.save(df, path)
        # Reload
        df2 = pd.read_csv(path)
        assert len(df2) == len(df)
        assert list(df2.columns) == list(df.columns)
    finally:
        os.unlink(path)
