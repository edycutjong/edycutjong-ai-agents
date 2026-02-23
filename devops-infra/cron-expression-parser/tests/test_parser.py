"""Tests for Cron Expression Parser."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.parser import parse_cron, parse_field, validate_cron, get_next_descriptions, format_result_markdown, PRESETS

def test_every_minute():
    r = parse_cron("* * * * *")
    assert r.is_valid and "every minute" in r.description.lower()

def test_specific_time():
    r = parse_cron("30 9 * * *")
    assert r.is_valid and r.fields[0].values == [30]

def test_range():
    f = parse_field("1-5", "day_of_week")
    assert f.values == [1, 2, 3, 4, 5]

def test_step():
    f = parse_field("*/15", "minute")
    assert 0 in f.values and 15 in f.values and 30 in f.values

def test_list():
    f = parse_field("1,15", "day_of_month")
    assert f.values == [1, 15]

def test_wildcard():
    f = parse_field("*", "hour")
    assert f.is_wildcard

def test_preset_daily():
    r = parse_cron("@daily")
    assert r.is_valid

def test_preset_hourly():
    r = parse_cron("@hourly")
    assert r.is_valid

def test_preset_weekly():
    r = parse_cron("@weekly")
    assert r.is_valid

def test_preset_monthly():
    r = parse_cron("@monthly")
    assert r.is_valid

def test_invalid_fields():
    r = parse_cron("* * *")
    assert not r.is_valid

def test_validate_valid():
    ok, err = validate_cron("0 0 * * *")
    assert ok and not err

def test_validate_invalid():
    ok, err = validate_cron("bad")
    assert not ok

def test_description():
    d = get_next_descriptions("0 9 * * 1")
    assert "Monday" in d or "9" in d

def test_month_names():
    f = parse_field("1,6", "month")
    assert "January" in f.description

def test_format_valid():
    r = parse_cron("*/5 * * * *")
    md = format_result_markdown(r)
    assert "✅" in md

def test_format_invalid():
    r = parse_cron("bad expr")
    md = format_result_markdown(r)
    assert "❌" in md

def test_to_dict():
    r = parse_cron("0 0 * * *")
    d = r.to_dict()
    assert "expression" in d and "description" in d

def test_presets_count():
    assert len(PRESETS) >= 6
