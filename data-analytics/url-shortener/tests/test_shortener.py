"""Tests for URL Shortener."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.shortener import URLStore, is_valid_url, bulk_shorten, format_result_markdown

def test_shorten(): s = URLStore(); r = s.shorten("https://example.com"); assert len(r.short_code) == 6
def test_resolve(): s = URLStore(); r = s.shorten("https://a.com"); assert s.resolve(r.short_code) == "https://a.com"
def test_dedup(): s = URLStore(); r1 = s.shorten("https://a.com"); r2 = s.shorten("https://a.com"); assert r1.short_code == r2.short_code
def test_unique(): s = URLStore(); r1 = s.shorten("https://a.com"); r2 = s.shorten("https://b.com"); assert r1.short_code != r2.short_code
def test_full_short(): s = URLStore(); r = s.shorten("https://x.com"); assert "short.ly" in r.full_short
def test_invalid(): s = URLStore(); r = s.shorten("not-a-url"); assert not r.is_valid
def test_valid_url(): assert is_valid_url("https://example.com")
def test_invalid_url(): assert not is_valid_url("ftp://bad")
def test_stats(): s = URLStore(); s.shorten("https://a.com"); s.shorten("https://b.com"); assert s.stats()["total_urls"] == 2
def test_resolve_missing(): s = URLStore(); assert s.resolve("xyz") == ""
def test_bulk(): results = bulk_shorten(["https://a.com", "https://b.com"]); assert len(results) == 2
def test_bulk_valid(): results = bulk_shorten(["https://a.com"]); assert results[0].is_valid
def test_code_length(): s = URLStore(); r = s.shorten("https://x.com/long/path"); assert len(r.short_code) >= 6
def test_format(): md = format_result_markdown(URLStore().shorten("https://x.com")); assert "URL Shortener" in md
def test_to_dict(): d = URLStore().shorten("https://x.com").to_dict(); assert "short_code" in d
