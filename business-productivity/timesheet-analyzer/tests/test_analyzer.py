"""Tests for Timesheet Analyzer."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.analyzer import TimeEntry, parse_csv_timesheet, analyze_timesheet, get_project_breakdown, format_report_markdown

CSV_DATA = """date,project,hours,description
2026-02-10,Backend,6,API development
2026-02-10,Meetings,2,Sprint planning
2026-02-11,Backend,7,Database migration
2026-02-11,Frontend,1,Bug fix
2026-02-12,Backend,4,Code review
2026-02-12,Frontend,3,UI polish
2026-02-12,Meetings,1.5,Standup
2026-02-13,Backend,8,Feature release
2026-02-14,Frontend,5,Testing
2026-02-14,DevOps,3,Deploy pipeline
"""

def test_parse_csv():
    entries = parse_csv_timesheet(CSV_DATA)
    assert len(entries) == 10

def test_parse_hours():
    entries = parse_csv_timesheet(CSV_DATA)
    assert all(e.hours > 0 for e in entries)

def test_parse_projects():
    entries = parse_csv_timesheet(CSV_DATA)
    projects = set(e.project for e in entries)
    assert "Backend" in projects
    assert "Frontend" in projects

def test_total_hours():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    assert report.total_hours == 40.5

def test_project_breakdown():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    assert report.project_hours["Backend"] == 25

def test_daily_hours():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    assert report.daily_hours["2026-02-10"] == 8

def test_avg_daily():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    assert report.avg_daily > 0

def test_utilization():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    assert 0 < report.utilization <= 150

def test_anomaly_high():
    entries = [TimeEntry(date="2026-01-01", project="X", hours=14)]
    report = analyze_timesheet(entries)
    assert len(report.anomalies) >= 1

def test_anomaly_low():
    entries = [TimeEntry(date="2026-01-01", project="X", hours=1)]
    report = analyze_timesheet(entries)
    assert any("missing" in a.lower() for a in report.anomalies)

def test_percentage_breakdown():
    entries = parse_csv_timesheet(CSV_DATA)
    breakdown = get_project_breakdown(entries)
    assert sum(breakdown.values()) == pytest.approx(100.0, abs=0.5)

def test_format_markdown():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    md = format_report_markdown(report)
    assert "Timesheet Report" in md
    assert "Backend" in md

def test_to_dict():
    entries = parse_csv_timesheet(CSV_DATA)
    report = analyze_timesheet(entries)
    d = report.to_dict()
    assert "total_hours" in d

def test_empty():
    report = analyze_timesheet([])
    assert report.total_hours == 0

def test_entry_to_dict():
    e = TimeEntry(date="2026-01-01", project="X", hours=5)
    d = e.to_dict()
    assert d["hours"] == 5
