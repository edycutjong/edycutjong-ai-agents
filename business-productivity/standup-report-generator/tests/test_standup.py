"""Tests for Standup Report Generator."""
import sys, os, json, tempfile, pytest
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.standup import (
    StandupEntry, StandupStorage,
    generate_daily_report, generate_weekly_summary, generate_blocker_report,
)

@pytest.fixture
def temp_path():
    with tempfile.TemporaryDirectory() as d:
        yield os.path.join(d, "test.json")

@pytest.fixture
def sample_entries():
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        StandupEntry(author="Alice", date=today, yesterday=["Fixed bug #42"], today=["Deploy v2.1"], blockers=["Waiting on API key"], mood="🟢"),
        StandupEntry(author="Bob", date=today, yesterday=["Code review"], today=["Write tests", "Update docs"], blockers=[], mood="🟡"),
        StandupEntry(author="Alice", date="2026-02-18", yesterday=["Sprint planning"], today=["Fix bug #42"], blockers=["Staging down"]),
    ]

# --- Entry Tests ---
def test_entry_auto_id():
    e = StandupEntry(author="Test")
    assert e.id != ""

def test_entry_auto_date():
    e = StandupEntry(author="Test")
    assert e.date == datetime.now().strftime("%Y-%m-%d")

def test_entry_roundtrip():
    e = StandupEntry(author="Alice", today=["Task A"], blockers=["Blocker 1"])
    d = e.to_dict()
    restored = StandupEntry.from_dict(d)
    assert restored.author == "Alice"
    assert restored.today == ["Task A"]

# --- Storage Tests ---
def test_add_and_retrieve(temp_path, sample_entries):
    s = StandupStorage(filepath=temp_path)
    s.add(sample_entries[0])
    assert len(s.get_all()) == 1

def test_get_by_date(temp_path, sample_entries):
    s = StandupStorage(filepath=temp_path)
    for e in sample_entries: s.add(e)
    today = datetime.now().strftime("%Y-%m-%d")
    results = s.get_by_date(today)
    assert len(results) == 2

def test_get_by_author(temp_path, sample_entries):
    s = StandupStorage(filepath=temp_path)
    for e in sample_entries: s.add(e)
    assert len(s.get_by_author("Alice")) == 2

def test_clear(temp_path, sample_entries):
    s = StandupStorage(filepath=temp_path)
    s.add(sample_entries[0])
    s.clear()
    assert len(s.get_all()) == 0

# --- Report Tests ---
def test_daily_report(sample_entries):
    today = datetime.now().strftime("%Y-%m-%d")
    report = generate_daily_report(sample_entries, today)
    assert "Daily Standup" in report
    assert "Alice" in report
    assert "Bob" in report
    assert "Deploy v2.1" in report

def test_daily_report_empty():
    report = generate_daily_report([], "2026-01-01")
    assert "No standup reports" in report

def test_daily_blockers_section(sample_entries):
    today = datetime.now().strftime("%Y-%m-%d")
    report = generate_daily_report(sample_entries, today)
    assert "Active Blockers" in report
    assert "API key" in report

def test_weekly_summary(sample_entries):
    summary = generate_weekly_summary(sample_entries)
    assert "Weekly Standup" in summary
    assert "Alice" in summary

def test_blocker_report_with_blockers(sample_entries):
    report = generate_blocker_report(sample_entries)
    assert "Blocker Report" in report
    assert "API key" in report
    assert "Staging down" in report

def test_blocker_report_none():
    entries = [StandupEntry(author="Happy", today=["Ship it"], blockers=[])]
    report = generate_blocker_report(entries)
    assert "No active blockers" in report

def test_mood_in_report(sample_entries):
    today = datetime.now().strftime("%Y-%m-%d")
    report = generate_daily_report(sample_entries, today)
    assert "🟢" in report

def test_tags_in_report():
    e = StandupEntry(author="Dev", today=["Work"], tags=["backend", "api"])
    report = generate_daily_report([e], e.date)
    assert "backend" in report
