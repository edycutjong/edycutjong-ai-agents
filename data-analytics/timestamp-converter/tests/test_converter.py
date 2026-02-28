"""Tests for Timestamp Converter."""
import sys, os, pytest, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import unix_to_datetime, iso_to_unix, now_utc, time_difference, add_time, is_future, format_relative, format_result_markdown

def test_unix_epoch(): r = unix_to_datetime(0); assert r.is_valid and "1970" in r.iso
def test_unix_known(): r = unix_to_datetime(1609459200); assert "2021" in r.iso
def test_unix_day(): r = unix_to_datetime(0); assert r.day_of_week == "Thursday"
def test_unix_invalid(): r = unix_to_datetime(1e20); assert not r.is_valid
def test_iso_parse(): r = iso_to_unix("2021-01-01T00:00:00+00:00"); assert abs(r.unix - 1609459200) < 1
def test_iso_invalid(): r = iso_to_unix("not-a-date"); assert not r.is_valid
def test_now(): r = now_utc(); assert r.is_valid and r.unix > 0
def test_diff(): d = time_difference(0, 3600); assert abs(d["hours"] - 1) < 0.01
def test_diff_days(): d = time_difference(0, 86400); assert abs(d["days"] - 1) < 0.01
def test_add_days(): r = add_time(0, days=1); assert r.unix == 86400
def test_add_hours(): r = add_time(0, hours=2); assert r.unix == 7200
def test_future(): assert is_future(time.time() + 10000)
def test_not_future(): assert not is_future(0)
def test_relative_now(): s = format_relative(time.time()); assert "just now" in s
def test_relative_past(): s = format_relative(time.time() - 7200); assert "hours ago" in s
def test_roundtrip(): r1 = unix_to_datetime(1609459200); r2 = iso_to_unix(r1.iso); assert abs(r2.unix - 1609459200) < 1
def test_format(): md = format_result_markdown(unix_to_datetime(0)); assert "Timestamp" in md
def test_to_dict(): d = unix_to_datetime(0).to_dict(); assert "unix" in d
