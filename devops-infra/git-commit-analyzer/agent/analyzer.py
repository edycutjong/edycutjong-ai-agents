"""Git commit analyzer — analyze commit history for patterns and quality."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from collections import Counter

CONVENTIONAL_TYPES = ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]

@dataclass
class CommitInfo:
    hash: str = ""
    message: str = ""
    commit_type: str = ""
    scope: str = ""
    is_breaking: bool = False
    is_conventional: bool = False

@dataclass
class CommitAnalysis:
    total: int = 0
    conventional_count: int = 0
    conventional_pct: float = 0.0
    type_distribution: dict = field(default_factory=dict)
    breaking_changes: int = 0
    avg_message_length: float = 0.0
    issues: list[str] = field(default_factory=list)
    score: int = 0  # 0-100

def parse_commit(line: str) -> CommitInfo:
    c = CommitInfo()
    parts = line.strip().split(" ", 1)
    if len(parts) == 2:
        c.hash = parts[0][:8]
        c.message = parts[1]
    else:
        c.message = line.strip()
    # Parse conventional commit
    m = re.match(r"^(\w+)(?:\(([^)]+)\))?(!?):\s*(.+)$", c.message)
    if m:
        ctype = m.group(1).lower()
        if ctype in CONVENTIONAL_TYPES:
            c.commit_type = ctype
            c.scope = m.group(2) or ""
            c.is_breaking = bool(m.group(3))
            c.is_conventional = True
    if "BREAKING CHANGE" in c.message: c.is_breaking = True
    return c

def parse_commits(text: str) -> list[CommitInfo]:
    return [parse_commit(line) for line in text.strip().split("\n") if line.strip()]

def analyze_commits(commits: list[CommitInfo]) -> CommitAnalysis:
    a = CommitAnalysis(total=len(commits))
    type_counter = Counter()
    msg_lengths = []
    for c in commits:
        if c.is_conventional: a.conventional_count += 1
        if c.commit_type: type_counter[c.commit_type] += 1
        if c.is_breaking: a.breaking_changes += 1
        msg_lengths.append(len(c.message))
    a.conventional_pct = round(a.conventional_count / max(a.total, 1) * 100, 1)
    a.type_distribution = dict(type_counter.most_common())
    a.avg_message_length = round(sum(msg_lengths) / max(len(msg_lengths), 1), 1)
    # Quality scoring
    score = 0
    if a.conventional_pct >= 80: score += 40
    elif a.conventional_pct >= 50: score += 25
    elif a.conventional_pct >= 20: score += 10
    if a.avg_message_length >= 10: score += 20
    if a.avg_message_length >= 30: score += 10
    if len(a.type_distribution) >= 3: score += 15
    if a.total >= 5: score += 15
    a.score = min(100, score)
    # Issues
    if a.conventional_pct < 50: a.issues.append("Low conventional commit adoption")
    if a.avg_message_length < 10: a.issues.append("Commit messages are too short")
    short_msgs = sum(1 for c in commits if len(c.message) < 5)
    if short_msgs > 0: a.issues.append(f"{short_msgs} commits with very short messages")
    return a

def format_analysis_markdown(a: CommitAnalysis) -> str:
    emoji = "🟢" if a.score >= 70 else "🟡" if a.score >= 40 else "🔴"
    lines = [f"## Commit Analysis {emoji}", f"**Total:** {a.total} | **Conventional:** {a.conventional_pct}% | **Score:** {a.score}/100", ""]
    if a.type_distribution:
        lines.append("### Commit Types")
        for t, count in a.type_distribution.items(): lines.append(f"- **{t}:** {count}")
        lines.append("")
    lines.append(f"**Avg message length:** {a.avg_message_length} chars | **Breaking changes:** {a.breaking_changes}")
    if a.issues:
        lines.append("\n### Issues")
        for i in a.issues: lines.append(f"- ⚠️ {i}")
    return "\n".join(lines)
