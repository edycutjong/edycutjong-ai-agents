"""Tests for Log Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import parse_line, parse_logs, analyze_logs, filter_by_level, search_logs, normalize_level, format_analysis_markdown

ISO_LOG = """2024-01-15T10:30:00Z INFO Application started
2024-01-15T10:30:01Z ERROR Database connection failed
2024-01-15T10:30:02Z WARNING High memory usage detected
2024-01-15T10:30:03Z INFO Processing request
2024-01-15T10:30:04Z ERROR Timeout on API call
2024-01-15T10:30:05Z DEBUG Cache hit ratio: 0.85"""

def test_parse_iso():
    e = parse_line("2024-01-15T10:30:00Z INFO Application started")
    assert e.level == "INFO" and "started" in e.message

def test_parse_bracketed():
    e = parse_line("[2024-01-15 10:30:00] ERROR Something broke")
    assert e.level == "ERROR"

def test_parse_fallback():
    e = parse_line("some random ERROR message")
    assert e.level == "ERROR"

def test_normalize_err(): assert normalize_level("err") == "ERROR"
def test_normalize_warn(): assert normalize_level("warn") == "WARNING"

def test_parse_logs():
    entries = parse_logs(ISO_LOG)
    assert len(entries) == 6

def test_analyze_total():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    assert a.total_lines == 6

def test_analyze_levels():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    assert a.levels["ERROR"] == 2

def test_analyze_errors():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    assert len(a.errors) == 2

def test_analyze_warnings():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    assert len(a.warnings) == 1

def test_filter_errors():
    entries = parse_logs(ISO_LOG)
    errs = filter_by_level(entries, "error")
    assert len(errs) == 2

def test_filter_info():
    entries = parse_logs(ISO_LOG)
    infos = filter_by_level(entries, "info")
    assert len(infos) == 2

def test_search():
    entries = parse_logs(ISO_LOG)
    results = search_logs(entries, "database")
    assert len(results) == 1

def test_search_no_match():
    entries = parse_logs(ISO_LOG)
    results = search_logs(entries, "xyz123")
    assert len(results) == 0

def test_time_range():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    assert a.time_range[0] and a.time_range[1]

def test_to_dict():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    d = a.to_dict()
    assert "total_lines" in d

def test_format():
    entries = parse_logs(ISO_LOG)
    a = analyze_logs(entries)
    md = format_analysis_markdown(a)
    assert "Log Analysis" in md and "Errors" in md
