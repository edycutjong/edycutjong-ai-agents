"""Changelog generator — generate changelogs from commit-style messages."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from collections import defaultdict

CATEGORIES = {"feat": "Features", "fix": "Bug Fixes", "docs": "Documentation", "style": "Styling", "refactor": "Refactoring", "perf": "Performance", "test": "Tests", "chore": "Chores", "ci": "CI", "build": "Build"}

@dataclass
class ChangeEntry:
    type: str = ""; scope: str = ""; message: str = ""; breaking: bool = False; raw: str = ""

@dataclass
class ChangelogResult:
    version: str = ""; entries: list[ChangeEntry] = field(default_factory=list)
    grouped: dict = field(default_factory=dict); breaking_changes: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    def to_dict(self) -> dict: return {"version": self.version, "total": len(self.entries), "breaking": len(self.breaking_changes)}

def parse_commit(message: str) -> ChangeEntry:
    e = ChangeEntry(raw=message)
    m = re.match(r'^(\w+)(?:\(([^)]+)\))?(!)?\s*:\s*(.+)', message)
    if m:
        e.type, e.scope, bang, e.message = m.group(1), m.group(2) or "", bool(m.group(3)), m.group(4)
        if bang or "BREAKING CHANGE" in message: e.breaking = True
    else: e.type = "other"; e.message = message
    return e

def generate_changelog(messages: list[str], version: str = "Unreleased") -> ChangelogResult:
    r = ChangelogResult(version=version)
    grouped = defaultdict(list)
    type_counts = defaultdict(int)
    for msg in messages:
        entry = parse_commit(msg.strip())
        r.entries.append(entry)
        cat = CATEGORIES.get(entry.type, "Other")
        grouped[cat].append(entry)
        type_counts[entry.type] += 1
        if entry.breaking: r.breaking_changes.append(entry.message)
    r.grouped = dict(grouped)
    r.stats = dict(type_counts)
    return r

def suggest_version_bump(result: ChangelogResult) -> str:
    if result.breaking_changes: return "major"
    if "feat" in result.stats: return "minor"
    return "patch"

def format_changelog_markdown(r: ChangelogResult) -> str:
    lines = [f"# Changelog", f"\n## [{r.version}]", ""]
    if r.breaking_changes:
        lines.append("### ⚠️ Breaking Changes")
        for b in r.breaking_changes: lines.append(f"- {b}")
        lines.append("")
    for cat in ["Features", "Bug Fixes", "Performance", "Refactoring", "Documentation", "Tests", "Chores", "CI", "Build", "Other"]:
        if cat in r.grouped:
            lines.append(f"### {cat}")
            for e in r.grouped[cat]:
                scope = f"**{e.scope}:** " if e.scope else ""
                lines.append(f"- {scope}{e.message}")
            lines.append("")
    return "\n".join(lines)
