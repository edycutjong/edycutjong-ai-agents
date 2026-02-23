"""Regex tester — test regex patterns against text with match highlighting."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class Match:
    text: str; start: int; end: int; groups: list[str] = field(default_factory=list)

@dataclass
class RegexResult:
    pattern: str = ""; text: str = ""; matches: list[Match] = field(default_factory=list)
    is_valid: bool = True; error: str = ""; flags_used: list[str] = field(default_factory=list)
    match_count: int = 0
    def to_dict(self) -> dict: return {"pattern": self.pattern, "is_valid": self.is_valid, "match_count": self.match_count}

FLAG_MAP = {"i": re.IGNORECASE, "m": re.MULTILINE, "s": re.DOTALL, "x": re.VERBOSE}

def compile_pattern(pattern: str, flags: str = "") -> tuple[re.Pattern | None, str]:
    flag_val = 0
    for f in flags:
        if f in FLAG_MAP: flag_val |= FLAG_MAP[f]
    try: return re.compile(pattern, flag_val), ""
    except re.error as e: return None, str(e)

def run_regex_test(pattern: str, text: str, flags: str = "") -> RegexResult:
    r = RegexResult(pattern=pattern, text=text, flags_used=list(flags))
    compiled, err = compile_pattern(pattern, flags)
    if not compiled: r.is_valid = False; r.error = err; return r
    for m in compiled.finditer(text):
        r.matches.append(Match(text=m.group(), start=m.start(), end=m.end(), groups=list(m.groups())))
    r.match_count = len(r.matches)
    return r

def validate_pattern(pattern: str) -> tuple[bool, str]:
    _, err = compile_pattern(pattern)
    return (True, "") if not err else (False, err)

def extract_groups(pattern: str, text: str) -> list[dict]:
    compiled, _ = compile_pattern(pattern)
    if not compiled: return []
    results = []
    for m in compiled.finditer(text):
        results.append({"full": m.group(), "groups": list(m.groups()), "named": dict(m.groupdict())})
    return results

COMMON_PATTERNS = {
    "email": r'[\w.-]+@[\w.-]+\.\w+',
    "url": r'https?://[\w.-]+(?:/[\w.-]*)*',
    "ipv4": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    "phone": r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
    "date_iso": r'\d{4}-\d{2}-\d{2}',
    "hex_color": r'#[0-9a-fA-F]{3,6}\b',
}

def get_common_pattern(name: str) -> str:
    return COMMON_PATTERNS.get(name, "")

def format_result_markdown(r: RegexResult) -> str:
    if not r.is_valid: return f"## Regex Test ❌\n**Pattern:** `{r.pattern}`\n**Error:** {r.error}"
    emoji = "✅" if r.match_count > 0 else "⚠️"
    lines = [f"## Regex Test {emoji}", f"**Pattern:** `{r.pattern}` | **Matches:** {r.match_count}", ""]
    for i, m in enumerate(r.matches[:10]):
        lines.append(f"{i+1}. `{m.text}` (pos {m.start}-{m.end})")
        if m.groups: lines.append(f"   Groups: {m.groups}")
    return "\n".join(lines)
