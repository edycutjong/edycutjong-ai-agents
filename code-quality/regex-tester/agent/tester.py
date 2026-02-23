"""Core regex testing engine."""
from __future__ import annotations

import re
import json
from dataclasses import dataclass, asdict, field
from typing import Any


# Common regex patterns library
COMMON_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "url": r"https?://[^\s<>\"']+",
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "ipv6": r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}",
    "phone_us": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "phone_intl": r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
    "date_iso": r"\d{4}-\d{2}-\d{2}",
    "date_us": r"\d{2}/\d{2}/\d{4}",
    "time_24h": r"\b([01]?\d|2[0-3]):[0-5]\d(:[0-5]\d)?\b",
    "hex_color": r"#[0-9a-fA-F]{3,8}\b",
    "uuid": r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "zip_us": r"\b\d{5}(-\d{4})?\b",
    "mac_address": r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})",
    "semver": r"\bv?\d+\.\d+\.\d+(?:-[\w.]+)?\b",
    "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    "username": r"^[a-zA-Z0-9_]{3,20}$",
    "password_strong": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    "html_tag": r"<[^>]+>",
    "json_key": r'"([^"]+)"\s*:',
    "python_import": r"^(?:from\s+\S+\s+)?import\s+\S+",
    "env_var": r"\$\{?[A-Z_][A-Z0-9_]*\}?",
    "jwt": r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+",
}


@dataclass
class MatchResult:
    """Result of a single regex match."""
    match: str
    start: int
    end: int
    groups: tuple = ()
    group_dict: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TestResult:
    """Full result of testing a regex against input."""
    pattern: str
    input_text: str
    is_valid: bool = True
    error: str = ""
    match_count: int = 0
    matches: list[MatchResult] = field(default_factory=list)
    flags_used: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "pattern": self.pattern,
            "is_valid": self.is_valid,
            "error": self.error,
            "match_count": self.match_count,
            "matches": [m.to_dict() for m in self.matches],
            "flags_used": self.flags_used,
        }


def parse_flags(flag_str: str) -> int:
    """Convert flag string like 'gi' to re flags."""
    flag_map = {
        "i": re.IGNORECASE,
        "m": re.MULTILINE,
        "s": re.DOTALL,
        "x": re.VERBOSE,
    }
    flags = 0
    for char in flag_str:
        if char in flag_map:
            flags |= flag_map[char]
    return flags


def get_flag_names(flag_str: str) -> list[str]:
    """Convert flag chars to readable names."""
    names = {"i": "IGNORECASE", "m": "MULTILINE", "s": "DOTALL", "x": "VERBOSE"}
    return [names[c] for c in flag_str if c in names]


def run_regex_test(pattern: str, text: str, flags: str = "") -> TestResult:
    """Test a regex pattern against input text.

    Args:
        pattern: The regex pattern.
        text: The input text to test against.
        flags: Optional flags string (i=ignorecase, m=multiline, s=dotall, x=verbose).

    Returns:
        TestResult with all matches and metadata.
    """
    result = TestResult(pattern=pattern, input_text=text, flags_used=get_flag_names(flags))

    # Validate pattern
    try:
        compiled = re.compile(pattern, parse_flags(flags))
    except re.error as e:
        result.is_valid = False
        result.error = str(e)
        return result

    # Find all matches
    for m in compiled.finditer(text):
        match_result = MatchResult(
            match=m.group(),
            start=m.start(),
            end=m.end(),
            groups=m.groups(),
            group_dict=m.groupdict(),
        )
        result.matches.append(match_result)

    result.match_count = len(result.matches)
    return result


def validate_pattern(pattern: str) -> dict:
    """Validate a regex pattern without testing it."""
    try:
        compiled = re.compile(pattern)
        return {
            "valid": True,
            "pattern": pattern,
            "groups": compiled.groups,
            "group_names": list(compiled.groupindex.keys()),
        }
    except re.error as e:
        return {
            "valid": False,
            "pattern": pattern,
            "error": str(e),
        }


def batch_test(patterns: list[str], text: str, flags: str = "") -> list[TestResult]:
    """Test multiple patterns against the same text."""
    return [run_regex_test(p, text, flags) for p in patterns]


def explain_pattern(pattern: str) -> list[str]:
    """Generate a simple explanation of regex components."""
    explanations = {
        r"\d": "digit (0-9)",
        r"\w": "word character (a-z, A-Z, 0-9, _)",
        r"\s": "whitespace",
        r"\b": "word boundary",
        r".": "any character",
        r"*": "zero or more",
        r"+": "one or more",
        r"?": "zero or one (optional)",
        r"^": "start of string/line",
        r"$": "end of string/line",
        r"|": "OR",
        r"[": "character class start",
        r"]": "character class end",
        r"(": "group start",
        r")": "group end",
        r"{": "quantifier start",
        r"}": "quantifier end",
    }

    parts = []
    i = 0
    while i < len(pattern):
        # Check two-char sequences first
        if i + 1 < len(pattern) and pattern[i] == "\\":
            two = pattern[i:i+2]
            if two in explanations:
                parts.append(f"`{two}` → {explanations[two]}")
                i += 2
                continue
            parts.append(f"`{two}` → escaped character '{pattern[i+1]}'")
            i += 2
            continue

        char = pattern[i]
        if char in explanations:
            parts.append(f"`{char}` → {explanations[char]}")
        elif char.isalnum():
            parts.append(f"`{char}` → literal '{char}'")
        i += 1

    return parts


def format_result_markdown(result: TestResult) -> str:
    """Format a test result as Markdown."""
    lines = [
        f"# Regex Test: `{result.pattern}`",
        "",
        f"**Valid:** {'✅ Yes' if result.is_valid else '❌ No'}",
    ]

    if result.error:
        lines.append(f"**Error:** {result.error}")
        return "\n".join(lines)

    if result.flags_used:
        lines.append(f"**Flags:** {', '.join(result.flags_used)}")

    lines.append(f"**Matches:** {result.match_count}")
    lines.append("")

    if result.matches:
        lines.append("| # | Match | Position | Groups |")
        lines.append("|---|-------|----------|--------|")
        for i, m in enumerate(result.matches, 1):
            groups = ", ".join(str(g) for g in m.groups) if m.groups else "—"
            lines.append(f"| {i} | `{m.match}` | {m.start}-{m.end} | {groups} |")

    return "\n".join(lines)
