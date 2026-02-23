"""ASCII art generator — convert text to ASCII art banners."""
from __future__ import annotations
from dataclasses import dataclass

CHARSET = {
    "A": [" # ", "# #", "###", "# #", "# #"], "B": ["## ", "# #", "## ", "# #", "## "],
    "C": [" ##", "#  ", "#  ", "#  ", " ##"], "D": ["## ", "# #", "# #", "# #", "## "],
    "E": ["###", "#  ", "## ", "#  ", "###"], "F": ["###", "#  ", "## ", "#  ", "#  "],
    "G": [" ##", "#  ", "# #", "# #", " ##"], "H": ["# #", "# #", "###", "# #", "# #"],
    "I": ["###", " # ", " # ", " # ", "###"], "J": ["###", "  #", "  #", "# #", " # "],
    "K": ["# #", "## ", "#  ", "## ", "# #"], "L": ["#  ", "#  ", "#  ", "#  ", "###"],
    "M": ["# #", "###", "# #", "# #", "# #"], "N": ["# #", "###", "###", "# #", "# #"],
    "O": [" # ", "# #", "# #", "# #", " # "], "P": ["## ", "# #", "## ", "#  ", "#  "],
    "Q": [" # ", "# #", "# #", " # ", "  #"], "R": ["## ", "# #", "## ", "# #", "# #"],
    "S": [" ##", "#  ", " # ", "  #", "## "], "T": ["###", " # ", " # ", " # ", " # "],
    "U": ["# #", "# #", "# #", "# #", " # "], "V": ["# #", "# #", "# #", " # ", " # "],
    "W": ["# #", "# #", "# #", "###", "# #"], "X": ["# #", " # ", " # ", " # ", "# #"],
    "Y": ["# #", " # ", " # ", " # ", " # "], "Z": ["###", "  #", " # ", "#  ", "###"],
    "0": [" # ", "# #", "# #", "# #", " # "], "1": [" # ", "## ", " # ", " # ", "###"],
    "2": [" # ", "# #", "  #", " # ", "###"], "3": ["###", "  #", " ##", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"], "5": ["###", "#  ", "## ", "  #", "## "],
    "6": [" ##", "#  ", "## ", "# #", " # "], "7": ["###", "  #", " # ", " # ", " # "],
    "8": [" # ", "# #", " # ", "# #", " # "], "9": [" # ", "# #", " ##", "  #", "## "],
    " ": ["   ", "   ", "   ", "   ", "   "], "!": [" # ", " # ", " # ", "   ", " # "],
    ".": ["   ", "   ", "   ", "   ", " # "], "?": [" # ", "# #", "  #", " # ", " # "],
}

@dataclass
class ASCIIResult:
    text: str = ""; art: str = ""; char_used: str = "#"; width: int = 0; height: int = 5
    def to_dict(self) -> dict: return {"text": self.text, "width": self.width, "height": self.height}

def text_to_ascii(text: str, char: str = "#") -> ASCIIResult:
    r = ASCIIResult(text=text, char_used=char)
    lines = [[] for _ in range(5)]
    for c in text.upper():
        glyph = CHARSET.get(c, ["   "] * 5)
        for row in range(5):
            lines[row].append(glyph[row])
    art_lines = [" ".join(row) for row in lines]
    r.art = "\n".join(art_lines)
    if char != "#": r.art = r.art.replace("#", char)
    r.width = max(len(l) for l in art_lines) if art_lines else 0
    return r

def box_text(text: str, padding: int = 1) -> str:
    w = len(text) + padding * 2
    border = "+" + "-" * (w + 2) + "+"
    pad = " " * padding
    return f"{border}\n| {pad}{text}{pad} |\n{border}"

def banner(text: str, width: int = 40) -> str:
    pad = max(0, (width - len(text)) // 2)
    line = "=" * width
    return f"{line}\n{' ' * pad}{text}\n{line}"

def format_result_markdown(r: ASCIIResult) -> str:
    return f"## ASCII Art 🎨\n```\n{r.art}\n```"
