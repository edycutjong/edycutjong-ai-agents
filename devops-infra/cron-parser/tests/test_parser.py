"""Tests for Cron Parser."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.parser import parse_cron, is_valid_cron, next_runs, explain, format_result_markdown, PRESETS

def test_valid(): r = parse_cron("0 0 * * *"); assert r.is_valid
def test_invalid(): r = parse_cron("bad"); assert not r.is_valid
def test_too_few(): r = parse_cron("0 0 *"); assert not r.is_valid
def test_fields(): r = parse_cron("30 2 * * 1"); assert r.fields["minute"] == "30"
def test_hour(): r = parse_cron("0 12 * * *"); assert r.fields["hour"] == "12"
def test_preset_daily(): r = parse_cron("@daily"); assert r.is_valid
def test_preset_hourly(): r = parse_cron("@hourly"); assert r.is_valid
def test_preset_yearly(): r = parse_cron("@yearly"); assert r.is_valid
def test_is_valid(): assert is_valid_cron("*/5 * * * *")
def test_not_valid(): assert not is_valid_cron("abc")
def test_next_runs(): runs = next_runs("0 * * * *"); assert len(runs) == 5
def test_next_invalid(): runs = next_runs("bad"); assert runs == []
def test_explain(): desc = explain("0 0 * * *"); assert len(desc) > 0
def test_explain_invalid(): desc = explain("bad"); assert "Invalid" in desc
def test_presets(): assert len(PRESETS) >= 6
def test_format(): md = format_result_markdown(parse_cron("0 0 * * *")); assert "Cron Parser" in md
def test_to_dict(): d = parse_cron("0 0 * * *").to_dict(); assert "is_valid" in d
