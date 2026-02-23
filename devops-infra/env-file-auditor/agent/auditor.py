"""Env file auditor — validate, compare, and audit .env files."""
from __future__ import annotations
import os, re
from dataclasses import dataclass, field

@dataclass
class EnvEntry:
    key: str
    value: str = ""
    line: int = 0
    has_value: bool = True
    is_sensitive: bool = False
    def to_dict(self) -> dict:
        return {"key": self.key, "value": "****" if self.is_sensitive else self.value, "line": self.line, "sensitive": self.is_sensitive}

SENSITIVE_PATTERNS = ["password", "secret", "key", "token", "api_key", "apikey", "auth", "credential", "private"]

def parse_env(text: str) -> list[EnvEntry]:
    entries = []
    for i, line in enumerate(text.split("\n"), 1):
        line = line.strip()
        if not line or line.startswith("#"): continue
        if "=" not in line: continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        is_sensitive = any(p in key.lower() for p in SENSITIVE_PATTERNS)
        entries.append(EnvEntry(key=key, value=value, line=i, has_value=bool(value), is_sensitive=is_sensitive))
    return entries

def parse_env_file(filepath: str) -> list[EnvEntry]:
    with open(filepath) as f: return parse_env(f.read())

@dataclass
class AuditResult:
    entries: list[EnvEntry] = field(default_factory=list)
    missing_values: list[str] = field(default_factory=list)
    sensitive_exposed: list[str] = field(default_factory=list)
    duplicates: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)
    score: int = 100
    def to_dict(self) -> dict:
        return {"total": len(self.entries), "missing_values": self.missing_values, "sensitive_exposed": self.sensitive_exposed, "duplicates": self.duplicates, "issues": self.issues, "score": self.score}

def audit_env(text: str) -> AuditResult:
    entries = parse_env(text)
    result = AuditResult(entries=entries)
    seen = {}
    for e in entries:
        if not e.has_value:
            result.missing_values.append(e.key)
            result.issues.append(f"Missing value for {e.key} (line {e.line})")
        if e.is_sensitive and e.has_value and e.value not in ("", "${" + e.key + "}") and not e.value.startswith("$"):
            result.sensitive_exposed.append(e.key)
            result.issues.append(f"Sensitive key '{e.key}' has a hardcoded value (line {e.line})")
        if e.key in seen:
            result.duplicates.append(e.key)
            result.issues.append(f"Duplicate key '{e.key}' at lines {seen[e.key]} and {e.line}")
        seen[e.key] = e.line
    # Score
    deductions = len(result.missing_values) * 10 + len(result.sensitive_exposed) * 15 + len(result.duplicates) * 5
    result.score = max(0, 100 - deductions)
    return result

@dataclass
class CompareResult:
    only_in_a: list[str] = field(default_factory=list)
    only_in_b: list[str] = field(default_factory=list)
    common: list[str] = field(default_factory=list)
    different_values: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return self.__dict__.copy()

def compare_envs(text_a: str, text_b: str) -> CompareResult:
    entries_a = {e.key: e.value for e in parse_env(text_a)}
    entries_b = {e.key: e.value for e in parse_env(text_b)}
    result = CompareResult()
    all_keys = set(entries_a) | set(entries_b)
    for k in sorted(all_keys):
        in_a = k in entries_a
        in_b = k in entries_b
        if in_a and not in_b: result.only_in_a.append(k)
        elif in_b and not in_a: result.only_in_b.append(k)
        else:
            result.common.append(k)
            if entries_a[k] != entries_b[k]: result.different_values.append(k)
    return result

def generate_env_template(text: str) -> str:
    """Generate a .env.example from a .env file (strip values)."""
    entries = parse_env(text)
    lines = []
    for e in entries:
        if e.is_sensitive: lines.append(f"{e.key}=")
        else: lines.append(f"{e.key}={e.value}")
    return "\n".join(lines)

def format_audit_markdown(result: AuditResult) -> str:
    emoji = "✅" if result.score >= 80 else "⚠️" if result.score >= 50 else "❌"
    lines = [f"# Env File Audit {emoji}", f"**Score:** {result.score}/100 | **Entries:** {len(result.entries)}", ""]
    if result.issues:
        lines.append("## Issues")
        for issue in result.issues: lines.append(f"- ⚠️ {issue}")
    else:
        lines.append("✅ No issues found!")
    return "\n".join(lines)
