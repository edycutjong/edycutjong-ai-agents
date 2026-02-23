"""Color converter — convert between Hex, RGB, HSL, and HSV color formats."""
from __future__ import annotations
import re, colorsys
from dataclasses import dataclass

@dataclass
class ColorResult:
    hex: str = ""; rgb: tuple = (0,0,0); hsl: tuple = (0,0,0); hsv: tuple = (0,0,0)
    name: str = ""; is_valid: bool = True; error: str = ""
    def to_dict(self) -> dict: return {"hex": self.hex, "rgb": self.rgb, "hsl": self.hsl, "is_valid": self.is_valid}

NAMED_COLORS = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF", "white": "#FFFFFF", "black": "#000000",
    "yellow": "#FFFF00", "cyan": "#00FFFF", "magenta": "#FF00FF", "orange": "#FFA500", "purple": "#800080"}

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"

def rgb_to_hsl(r: int, g: int, b: int) -> tuple[int, int, int]:
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return round(h * 360), round(s * 100), round(l * 100)

def rgb_to_hsv(r: int, g: int, b: int) -> tuple[int, int, int]:
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return round(h * 360), round(s * 100), round(v * 100)

def parse_color(color: str) -> ColorResult:
    r = ColorResult()
    color = color.strip().lower()
    if color in NAMED_COLORS: r.name = color; color = NAMED_COLORS[color].lower()
    if re.match(r'^#?[0-9a-f]{3,6}$', color):
        if not color.startswith("#"): color = "#" + color
        r.hex = color.upper(); r.rgb = hex_to_rgb(color)
        r.hsl = rgb_to_hsl(*r.rgb); r.hsv = rgb_to_hsv(*r.rgb)
    elif m := re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color):
        r.rgb = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        r.hex = rgb_to_hex(*r.rgb); r.hsl = rgb_to_hsl(*r.rgb); r.hsv = rgb_to_hsv(*r.rgb)
    else:
        r.is_valid = False; r.error = f"Cannot parse: {color}"
    return r

def complement(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(255 - r, 255 - g, 255 - b)

def brightness(hex_color: str) -> float:
    r, g, b = hex_to_rgb(hex_color)
    return round((0.299 * r + 0.587 * g + 0.114 * b) / 255 * 100, 1)

def format_result_markdown(c: ColorResult) -> str:
    if not c.is_valid: return f"## Color Converter ❌\n**Error:** {c.error}"
    return f"## Color Converter 🎨\n**Hex:** `{c.hex}` | **RGB:** `{c.rgb}` | **HSL:** `{c.hsl}`"
