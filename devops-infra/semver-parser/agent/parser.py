"""Semver parser — parse, compare, and validate semantic versions."""
from __future__ import annotations
import re
from dataclasses import dataclass
from functools import total_ordering

@total_ordering
@dataclass
class SemVer:
    major: int = 0; minor: int = 0; patch: int = 0; prerelease: str = ""; build: str = ""
    raw: str = ""; is_valid: bool = True; error: str = ""
    def __str__(self): return f"{self.major}.{self.minor}.{self.patch}" + (f"-{self.prerelease}" if self.prerelease else "") + (f"+{self.build}" if self.build else "")
    def __eq__(self, other): return isinstance(other, SemVer) and (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
    def __lt__(self, other): return isinstance(other, SemVer) and (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
    def to_dict(self) -> dict: return {"major": self.major, "minor": self.minor, "patch": self.patch, "prerelease": self.prerelease, "is_valid": self.is_valid}

SEMVER_RE = re.compile(r'^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?$')

def parse_semver(version: str) -> SemVer:
    m = SEMVER_RE.match(version.strip())
    if not m: return SemVer(raw=version, is_valid=False, error=f"Invalid: {version}")
    return SemVer(major=int(m.group(1)), minor=int(m.group(2)), patch=int(m.group(3)), prerelease=m.group(4) or "", build=m.group(5) or "", raw=version, is_valid=True)

def bump(version: str, part: str = "patch") -> SemVer:
    v = parse_semver(version)
    if not v.is_valid: return v
    if part == "major": v.major += 1; v.minor = 0; v.patch = 0
    elif part == "minor": v.minor += 1; v.patch = 0
    else: v.patch += 1
    v.prerelease = ""; v.build = ""
    return v

def is_compatible(v1: str, v2: str) -> bool:
    a, b = parse_semver(v1), parse_semver(v2)
    return a.major == b.major

def sort_versions(versions: list[str]) -> list[str]:
    parsed = [(parse_semver(v), v) for v in versions]
    return [v for _, v in sorted(parsed, key=lambda x: (x[0].major, x[0].minor, x[0].patch))]

def satisfies_range(version: str, range_str: str) -> bool:
    v = parse_semver(version)
    if range_str.startswith("^"):
        target = parse_semver(range_str[1:])
        return v.major == target.major and v >= target
    elif range_str.startswith("~"):
        target = parse_semver(range_str[1:])
        return v.major == target.major and v.minor == target.minor and v >= target
    return parse_semver(range_str) == v

def format_result_markdown(v: SemVer) -> str:
    if not v.is_valid: return f"## SemVer ❌\n**Error:** {v.error}"
    return f"## SemVer ✅\n**Version:** `{v}` | **Major:** {v.major} | **Minor:** {v.minor} | **Patch:** {v.patch}"
