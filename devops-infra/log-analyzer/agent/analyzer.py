"""Log analyzer — parse, filter, and analyze log files."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from collections import Counter

@dataclass
class LogEntry:
    timestamp: str = ""
    level: str = ""
    message: str = ""
    source: str = ""
    raw: str = ""

@dataclass
class LogAnalysis:
    total_lines: int = 0
    levels: dict = field(default_factory=dict)
    errors: list[LogEntry] = field(default_factory=list)
    warnings: list[LogEntry] = field(default_factory=list)
    top_messages: list[tuple] = field(default_factory=list)
    time_range: tuple = ("", "")
    def to_dict(self) -> dict:
        return {"total_lines": self.total_lines, "levels": self.levels, "errors": len(self.errors), "warnings": len(self.warnings)}

LOG_PATTERNS = [
    re.compile(r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[^ ]*)\s+(\w+)\s+(.*)$"),  # ISO timestamp
    re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+(\w+)\s+(.*)$"),      # Bracketed
    re.compile(r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+(\w+):\s+(.*)$"),   # Syslog
    re.compile(r"^(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}[^ ]*)\s+(.*)$"),              # Apache-like
]

LEVEL_ALIASES = {"err": "ERROR", "error": "ERROR", "warn": "WARNING", "warning": "WARNING",
                 "info": "INFO", "debug": "DEBUG", "critical": "CRITICAL", "fatal": "FATAL",
                 "notice": "NOTICE", "trace": "TRACE"}

def parse_line(line: str) -> LogEntry:
    line = line.strip()
    if not line: return LogEntry(raw=line)
    for pattern in LOG_PATTERNS:
        m = pattern.match(line)
        if m:
            groups = m.groups()
            if len(groups) == 3:
                return LogEntry(timestamp=groups[0], level=normalize_level(groups[1]), message=groups[2], raw=line)
            elif len(groups) == 2:
                return LogEntry(timestamp=groups[0], message=groups[1], raw=line)
    # Fallback: check for level keywords
    for keyword in ["ERROR", "WARN", "INFO", "DEBUG", "CRITICAL", "FATAL"]:
        if keyword in line.upper():
            return LogEntry(level=normalize_level(keyword), message=line, raw=line)
    return LogEntry(message=line, raw=line)

def normalize_level(level: str) -> str:
    return LEVEL_ALIASES.get(level.lower(), level.upper())

def parse_logs(text: str) -> list[LogEntry]:
    return [parse_line(line) for line in text.strip().split("\n") if line.strip()]

def analyze_logs(entries: list[LogEntry]) -> LogAnalysis:
    a = LogAnalysis(total_lines=len(entries))
    level_counter = Counter()
    msg_counter = Counter()
    timestamps = []
    for e in entries:
        if e.level: level_counter[e.level] += 1
        if e.level == "ERROR": a.errors.append(e)
        elif e.level == "WARNING": a.warnings.append(e)
        if e.message: msg_counter[e.message[:80]] += 1
        if e.timestamp: timestamps.append(e.timestamp)
    a.levels = dict(level_counter.most_common())
    a.top_messages = msg_counter.most_common(10)
    if timestamps: a.time_range = (timestamps[0], timestamps[-1])
    return a

def filter_by_level(entries: list[LogEntry], level: str) -> list[LogEntry]:
    norm = normalize_level(level)
    return [e for e in entries if e.level == norm]

def search_logs(entries: list[LogEntry], query: str) -> list[LogEntry]:
    return [e for e in entries if query.lower() in e.message.lower()]

def format_analysis_markdown(a: LogAnalysis) -> str:
    lines = ["## Log Analysis", f"**Total Lines:** {a.total_lines} | **Errors:** {len(a.errors)} | **Warnings:** {len(a.warnings)}", ""]
    if a.levels:
        lines.append("### Level Distribution")
        for level, count in a.levels.items():
            lines.append(f"- **{level}:** {count}")
        lines.append("")
    if a.errors:
        lines.append("### Recent Errors")
        for e in a.errors[:5]:
            lines.append(f"- `{e.timestamp}` {e.message[:100]}")
        lines.append("")
    if a.top_messages:
        lines.append("### Top Repeated Messages")
        for msg, count in a.top_messages[:5]:
            lines.append(f"- ({count}x) {msg[:60]}")
    return "\n".join(lines)
