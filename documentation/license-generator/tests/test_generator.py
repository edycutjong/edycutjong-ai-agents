"""Tests for License Generator."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import generate, get_available, get_summary, format_result_markdown, LICENSES

def test_mit(): r = generate("MIT", "Dev", 2026); assert "MIT License" in r.content
def test_apache(): r = generate("Apache-2.0", "Dev"); assert "Apache" in r.content
def test_gpl(): r = generate("GPL-3.0", "Dev"); assert "GNU" in r.content
def test_bsd(): r = generate("BSD-3-Clause", "Dev"); assert "BSD" in r.content
def test_isc(): r = generate("ISC", "Dev"); assert "ISC" in r.content
def test_unlicense(): r = generate("Unlicense", "Dev"); assert "public domain" in r.content
def test_author(): r = generate("MIT", "Alice", 2026); assert "Alice" in r.content
def test_year(): r = generate("MIT", "Dev", 2025); assert "2025" in r.content
def test_unknown(): r = generate("Unknown", "Dev"); assert "Unknown license" in r.content
def test_available(): avail = get_available(); assert "MIT" in avail and len(avail) >= 6
def test_summary(): s = get_summary("MIT"); assert "Permissive" in s
def test_summary_unknown(): s = get_summary("X"); assert "Unknown" in s
def test_templates(): assert len(LICENSES) >= 6
def test_format(): md = format_result_markdown(generate("MIT", "Dev")); assert "License Generator" in md
def test_to_dict(): d = generate("MIT", "Dev").to_dict(); assert "type" in d
