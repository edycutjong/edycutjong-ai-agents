"""Color palette generator — generate harmonious color palettes from a base color."""
from __future__ import annotations
import re, colorsys
from dataclasses import dataclass, field

@dataclass
class Color:
    hex: str = ""; r: int = 0; g: int = 0; b: int = 0; h: float = 0; s: float = 0; l: float = 0; name: str = ""

@dataclass
class PaletteResult:
    base_color: Color = field(default_factory=Color); colors: list[Color] = field(default_factory=list)
    scheme: str = ""; count: int = 0
    def to_dict(self) -> dict: return {"scheme": self.scheme, "count": self.count, "colors": [c.hex for c in self.colors]}

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return h * 360, s * 100, l * 100

def hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)

def make_color(hex_color: str) -> Color:
    r, g, b = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(r, g, b)
    return Color(hex=hex_color.lower(), r=r, g=g, b=b, h=h, s=s, l=l)

def complementary(base: str) -> PaletteResult:
    c = make_color(base); h, s, l = c.h, c.s, c.l
    comp_h = (h + 180) % 360
    r2, g2, b2 = hsl_to_rgb(comp_h, s, l)
    colors = [c, make_color(rgb_to_hex(r2, g2, b2))]
    return PaletteResult(base_color=c, colors=colors, scheme="complementary", count=2)

def analogous(base: str) -> PaletteResult:
    c = make_color(base); h, s, l = c.h, c.s, c.l
    colors = [c]
    for offset in [-30, 30]:
        new_h = (h + offset) % 360
        r, g, b = hsl_to_rgb(new_h, s, l)
        colors.append(make_color(rgb_to_hex(r, g, b)))
    return PaletteResult(base_color=c, colors=colors, scheme="analogous", count=3)

def triadic(base: str) -> PaletteResult:
    c = make_color(base); h, s, l = c.h, c.s, c.l
    colors = [c]
    for offset in [120, 240]:
        new_h = (h + offset) % 360
        r, g, b = hsl_to_rgb(new_h, s, l)
        colors.append(make_color(rgb_to_hex(r, g, b)))
    return PaletteResult(base_color=c, colors=colors, scheme="triadic", count=3)

def monochromatic(base: str, count: int = 5) -> PaletteResult:
    c = make_color(base); h, s, l = c.h, c.s, c.l
    colors = []
    for i in range(count):
        new_l = max(10, min(90, 20 + (60 / max(count - 1, 1)) * i))
        r, g, b = hsl_to_rgb(h, s, new_l)
        colors.append(make_color(rgb_to_hex(r, g, b)))
    return PaletteResult(base_color=c, colors=colors, scheme="monochromatic", count=count)

def generate_palette(base: str, scheme: str = "complementary") -> PaletteResult:
    schemes = {"complementary": complementary, "analogous": analogous, "triadic": triadic, "monochromatic": monochromatic}
    func = schemes.get(scheme, complementary)
    return func(base)

def format_result_markdown(r: PaletteResult) -> str:
    lines = [f"## Color Palette 🎨", f"**Base:** `{r.base_color.hex}` | **Scheme:** {r.scheme} | **Colors:** {r.count}", ""]
    for c in r.colors: lines.append(f"- `{c.hex}` — RGB({c.r}, {c.g}, {c.b})")
    return "\n".join(lines)
