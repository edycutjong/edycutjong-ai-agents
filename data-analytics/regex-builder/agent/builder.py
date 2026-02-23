"""Regex builder — create, test, and explain regular expressions."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

COMMON_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "url": r"https?://[^\s<>\"']+",
    "phone_us": r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "date_iso": r"\d{4}-\d{2}-\d{2}",
    "date_us": r"\d{2}/\d{2}/\d{4}",
    "hex_color": r"#(?:[0-9a-fA-F]{3}){1,2}\b",
    "uuid": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "zip_us": r"\b\d{5}(?:-\d{4})?\b",
    "slug": r"[a-z0-9]+(?:-[a-z0-9]+)*",
    "username": r"[a-zA-Z][a-zA-Z0-9_]{2,15}",
    "semver": r"\bv?\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?\b",
}

@dataclass
class TestResult:
    pattern: str
    text: str
    matches: list[str] = field(default_factory=list)
    match_count: int = 0
    is_valid: bool = True
    error: str = ""
    def to_dict(self) -> dict:
        return {"pattern": self.pattern, "matches": self.matches, "match_count": self.match_count, "is_valid": self.is_valid, "error": self.error}

def run_test(pattern: str, text: str, flags: int = 0) -> TestResult:
    try:
        re.compile(pattern)
    except re.error as e:
        return TestResult(pattern=pattern, text=text, is_valid=False, error=str(e))
    matches = re.findall(pattern, text, flags)
    return TestResult(pattern=pattern, text=text, matches=matches, match_count=len(matches))

def get_pattern(name: str) -> str | None:
    return COMMON_PATTERNS.get(name.lower().replace(" ", "_"))

def list_patterns() -> list[str]:
    return sorted(COMMON_PATTERNS.keys())

def explain_pattern(pattern: str) -> str:
    """Provide a simplified explanation of regex components."""
    explanations = {
        r"\d": "digit (0-9)", r"\w": "word character (a-z, A-Z, 0-9, _)", r"\s": "whitespace",
        r"\b": "word boundary", r".": "any character", r"^": "start of string", r"$": "end of string",
        r"+": "one or more", r"*": "zero or more", r"?": "optional (0 or 1)",
        r"\d+": "one or more digits", r"\w+": "one or more word chars", r"\s+": "one or more spaces",
    }
    parts = []
    for token, desc in explanations.items():
        if token in pattern:
            parts.append(f"- `{token}` → {desc}")
    groups = re.findall(r"\((?:\?:)?(.*?)\)", pattern)
    for g in groups:
        parts.append(f"- `({g})` → capture group")
    char_classes = re.findall(r"\[([^\]]+)\]", pattern)
    for cc in char_classes:
        parts.append(f"- `[{cc}]` → character set")
    quantifiers = re.findall(r"\{(\d+(?:,\d*)?)\}", pattern)
    for q in quantifiers:
        parts.append(f"- `{{{q}}}` → repeat {q} times")
    return "\n".join(parts) if parts else "Simple literal pattern"

def build_pattern(components: list[str]) -> str:
    """Build a pattern from named components."""
    return "".join(get_pattern(c) or c for c in components)

def validate_pattern(pattern: str) -> tuple[bool, str]:
    try:
        re.compile(pattern)
        return True, "Valid regex"
    except re.error as e:
        return False, str(e)

def format_test_markdown(result: TestResult) -> str:
    lines = [f"## Regex Test", f"**Pattern:** `{result.pattern}`"]
    if not result.is_valid:
        lines.append(f"❌ Invalid: {result.error}")
    elif result.matches:
        lines.append(f"✅ **{result.match_count} matches found**")
        for m in result.matches[:20]:
            lines.append(f"- `{m}`")
    else:
        lines.append("⚠️ No matches found")
    return "\n".join(lines)
