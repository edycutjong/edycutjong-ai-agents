"""Tests for ASCII Art Generator."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import text_to_ascii, box_text, banner, format_result_markdown, CHARSET

def test_hello(): r = text_to_ascii("HI"); assert "#" in r.art
def test_height(): r = text_to_ascii("A"); assert r.art.count("\n") == 4
def test_custom_char(): r = text_to_ascii("A", char="*"); assert "*" in r.art and "#" not in r.art
def test_space(): r = text_to_ascii("A B"); assert r.width > 0
def test_numbers(): r = text_to_ascii("123"); assert "#" in r.art
def test_upper(): r = text_to_ascii("hi"); assert "#" in r.art  # auto uppercases
def test_width(): r = text_to_ascii("AB"); assert r.width > 0
def test_empty(): r = text_to_ascii(""); assert r.art == "\n\n\n\n"
def test_charset(): assert len(CHARSET) >= 36
def test_box(): b = box_text("Hello"); assert "+" in b and "Hello" in b
def test_box_border(): b = box_text("X"); assert b.startswith("+") and b.endswith("+")
def test_banner(): b = banner("Test"); assert "=" in b and "Test" in b
def test_banner_width(): b = banner("X", width=20); assert len(b.split("\n")[0]) == 20
def test_format(): md = format_result_markdown(text_to_ascii("HI")); assert "ASCII Art" in md
def test_to_dict(): d = text_to_ascii("HI").to_dict(); assert "width" in d
def test_punct(): r = text_to_ascii("HI!"); assert "#" in r.art
