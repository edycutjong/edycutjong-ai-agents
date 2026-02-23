"""Tests for Color Palette Generator."""
import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent.generator import hex_to_rgb, rgb_to_hex, rgb_to_hsl, hsl_to_rgb, make_color, complementary, analogous, triadic, monochromatic, generate_palette, format_result_markdown

def test_hex_to_rgb(): assert hex_to_rgb("#ff0000") == (255, 0, 0)
def test_hex_short(): assert hex_to_rgb("#f00") == (255, 0, 0)
def test_rgb_to_hex(): assert rgb_to_hex(255, 0, 0) == "#ff0000"
def test_hsl_roundtrip(): h, s, l = rgb_to_hsl(128, 64, 192); r, g, b = hsl_to_rgb(h, s, l); assert abs(r - 128) <= 1
def test_make_color(): c = make_color("#ff0000"); assert c.r == 255 and c.g == 0 and c.hex == "#ff0000"
def test_complementary(): p = complementary("#ff0000"); assert p.count == 2 and len(p.colors) == 2
def test_comp_opposite(): p = complementary("#ff0000"); assert p.colors[1].hex != "#ff0000"
def test_analogous(): p = analogous("#ff0000"); assert p.count == 3 and p.scheme == "analogous"
def test_triadic(): p = triadic("#ff0000"); assert p.count == 3 and p.scheme == "triadic"
def test_mono(): p = monochromatic("#3366cc"); assert p.count == 5 and len(p.colors) == 5
def test_mono_count(): p = monochromatic("#3366cc", count=3); assert p.count == 3
def test_generate_default(): p = generate_palette("#ff0000"); assert p.scheme == "complementary"
def test_generate_triadic(): p = generate_palette("#ff0000", "triadic"); assert p.scheme == "triadic"
def test_format(): md = format_result_markdown(complementary("#3366cc")); assert "Color Palette" in md
def test_to_dict(): d = complementary("#ff0000").to_dict(); assert "scheme" in d and "colors" in d
