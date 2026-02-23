"""Release notes generator — create changelogs from commit messages."""
from __future__ import annotations
import re, json
from dataclasses import dataclass, field
from datetime import datetime

CONVENTIONAL_PATTERN = re.compile(r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?: (?P<description>.+)$")

@dataclass
class CommitInfo:
    hash: str = ""
    message: str = ""
    type: str = "other"
    scope: str = ""
    description: str = ""
    breaking: bool = False
    author: str = ""
    date: str = ""
    def to_dict(self) -> dict:
        return self.__dict__.copy()

CATEGORY_LABELS = {"feat": "🚀 Features", "fix": "🐛 Bug Fixes", "docs": "📚 Documentation", "perf": "⚡ Performance", "refactor": "♻️ Refactoring", "test": "🧪 Tests", "build": "📦 Build", "ci": "🔧 CI/CD", "chore": "🔨 Chores", "style": "💅 Style", "revert": "⏪ Reverts", "other": "📋 Other"}

def parse_commit(message: str, hash: str = "", author: str = "", date: str = "") -> CommitInfo:
    m = CONVENTIONAL_PATTERN.match(message.strip())
    if m:
        return CommitInfo(hash=hash, message=message, type=m.group("type"), scope=m.group("scope") or "", description=m.group("description"), breaking=bool(m.group("breaking")), author=author, date=date)
    return CommitInfo(hash=hash, message=message, description=message, author=author, date=date)

def parse_commits(text: str) -> list[CommitInfo]:
    """Parse newline-separated commit messages."""
    commits = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line: continue
        parts = line.split(" ", 1)
        if len(parts) == 2 and len(parts[0]) >= 7 and all(c in "0123456789abcdef" for c in parts[0]):
            commits.append(parse_commit(parts[1], hash=parts[0]))
        else:
            commits.append(parse_commit(line))
    return commits

def group_by_type(commits: list[CommitInfo]) -> dict[str, list[CommitInfo]]:
    groups = {}
    for c in commits:
        groups.setdefault(c.type, []).append(c)
    return groups

def generate_release_notes(commits: list[CommitInfo], version: str = "Unreleased", date: str = "") -> str:
    if not date: date = datetime.now().strftime("%Y-%m-%d")
    groups = group_by_type(commits)
    lines = [f"# {version} ({date})", ""]
    # Breaking changes first
    breaking = [c for c in commits if c.breaking]
    if breaking:
        lines.append("## ⚠️ BREAKING CHANGES")
        for c in breaking:
            scope = f"**{c.scope}:** " if c.scope else ""
            lines.append(f"- {scope}{c.description}")
        lines.append("")
    # Grouped sections
    order = ["feat", "fix", "perf", "refactor", "docs", "test", "build", "ci", "chore", "style", "revert", "other"]
    for cat in order:
        if cat not in groups: continue
        label = CATEGORY_LABELS.get(cat, cat)
        lines.append(f"## {label}")
        for c in groups[cat]:
            scope = f"**{c.scope}:** " if c.scope else ""
            hash_ref = f" ({c.hash[:7]})" if c.hash else ""
            lines.append(f"- {scope}{c.description}{hash_ref}")
        lines.append("")
    return "\n".join(lines)

def get_stats(commits: list[CommitInfo]) -> dict:
    groups = group_by_type(commits)
    return {"total": len(commits), "features": len(groups.get("feat", [])), "fixes": len(groups.get("fix", [])),
            "breaking": sum(1 for c in commits if c.breaking), "types": len(groups)}
