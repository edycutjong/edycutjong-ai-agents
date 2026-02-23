"""Tests for Color Converter."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.converter import parse_color, hex_to_rgb, rgb_to_hex, rgb_to_hsl, rgb_to_hsv, complement, brightness, format_result_markdown, NAMED_COLORS

def test_hex(): c = parse_color("#FF0000"); assert c.rgb == (255, 0, 0)
def test_hex_no_hash(): c = parse_color("FF0000"); assert c.rgb == (255, 0, 0)
def test_shorthand(): c = parse_color("#F00"); assert c.rgb == (255, 0, 0)
def test_rgb_format(): c = parse_color("rgb(255, 0, 0)"); assert c.hex == "#FF0000"
def test_named(): c = parse_color("red"); assert c.rgb == (255, 0, 0)
def test_invalid(): c = parse_color("not-a-color"); assert not c.is_valid
def test_hex_to_rgb(): assert hex_to_rgb("#00FF00") == (0, 255, 0)
def test_rgb_to_hex(): assert rgb_to_hex(0, 0, 255) == "#0000FF"
def test_hsl(): h, s, l = rgb_to_hsl(255, 0, 0); assert h == 0 and s == 100
def test_hsv(): h, s, v = rgb_to_hsv(255, 0, 0); assert h == 0 and v == 100
def test_complement(): assert complement("#FF0000") == "#00FFFF"
def test_brightness_white(): assert brightness("#FFFFFF") == 100.0
def test_brightness_black(): assert brightness("#000000") == 0.0
def test_named_colors(): assert len(NAMED_COLORS) >= 10
def test_format(): md = format_result_markdown(parse_color("#FF0000")); assert "Color Converter" in md
def test_to_dict(): d = parse_color("#FF0000").to_dict(); assert "hex" in d
