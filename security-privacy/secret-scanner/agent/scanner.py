"""Secret scanner — detect leaked credentials and API keys in code."""
from __future__ import annotations
import re, os, json
from dataclasses import dataclass, field

@dataclass
class SecretMatch:
    file: str
    line: int
    rule: str
    match: str
    severity: str = "high"  # critical, high, medium, low
    def to_dict(self) -> dict:
        masked = self.match[:4] + "****" + self.match[-4:] if len(self.match) > 8 else "****"
        return {"file": self.file, "line": self.line, "rule": self.rule, "match_masked": masked, "severity": self.severity}

SECRET_PATTERNS = [
    {"name": "AWS Access Key", "pattern": r"AKIA[0-9A-Z]{16}", "severity": "critical"},
    {"name": "AWS Secret Key", "pattern": r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{40}['\"]", "severity": "critical"},
    {"name": "GitHub Token", "pattern": r"gh[ps]_[A-Za-z0-9_]{36,}", "severity": "critical"},
    {"name": "Generic API Key", "pattern": r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][A-Za-z0-9]{20,}['\"]", "severity": "high"},
    {"name": "Generic Secret", "pattern": r"(?i)(secret|password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]", "severity": "high"},
    {"name": "JWT Token", "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "severity": "high"},
    {"name": "Private Key", "pattern": r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "severity": "critical"},
    {"name": "Slack Token", "pattern": r"xox[bpors]-[0-9]{10,}-[A-Za-z0-9-]+", "severity": "critical"},
    {"name": "Stripe Key", "pattern": r"sk_(live|test)_[A-Za-z0-9_]{24,}", "severity": "critical"},
    {"name": "Database URL", "pattern": r"(?i)(postgres|mysql|mongodb)://[^\s'\"]{10,}", "severity": "high"},
    {"name": "Bearer Token", "pattern": r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{20,}", "severity": "medium"},
    {"name": "Hex Token 32+", "pattern": r"(?i)(token|key|secret)\s*[:=]\s*['\"][0-9a-f]{32,}['\"]", "severity": "medium"},
]

IGNORE_EXTENSIONS = {".pyc", ".png", ".jpg", ".gif", ".ico", ".woff", ".ttf", ".zip", ".gz", ".tar"}
IGNORE_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache", "dist", "build"}

def scan_text(text: str, filename: str = "<stdin>") -> list[SecretMatch]:
    """Scan text content for secrets."""
    matches = []
    for i, line in enumerate(text.split("\n"), 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("<!--"): continue
        for rule in SECRET_PATTERNS:
            for m in re.finditer(rule["pattern"], line):
                matches.append(SecretMatch(file=filename, line=i, rule=rule["name"], match=m.group(), severity=rule["severity"]))
    return matches

def scan_file(filepath: str) -> list[SecretMatch]:
    ext = os.path.splitext(filepath)[1].lower()
    if ext in IGNORE_EXTENSIONS: return []
    try:
        with open(filepath, "r", errors="ignore") as f: text = f.read()
        return scan_text(text, filepath)
    except: return []

def scan_directory(directory: str) -> list[SecretMatch]:
    all_matches = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fname in files:
            fpath = os.path.join(root, fname)
            all_matches.extend(scan_file(fpath))
    return all_matches

def get_severity_counts(matches: list[SecretMatch]) -> dict:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for m in matches: counts[m.severity] = counts.get(m.severity, 0) + 1
    return counts

def format_report_markdown(matches: list[SecretMatch]) -> str:
    counts = get_severity_counts(matches)
    lines = ["# Secret Scanner Report", f"**Findings:** {len(matches)} | 🔴 Critical: {counts['critical']} | 🟠 High: {counts['high']} | 🟡 Medium: {counts['medium']}", ""]
    severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "⚪"}
    for m in sorted(matches, key=lambda x: {"critical":0,"high":1,"medium":2,"low":3}.get(x.severity, 4)):
        e = severity_emoji.get(m.severity, "⬜")
        masked = m.match[:4] + "****" if len(m.match) > 4 else "****"
        lines.append(f"- {e} **{m.rule}** in `{m.file}:{m.line}` — `{masked}`")
    if not matches: lines.append("✅ No secrets detected!")
    return "\n".join(lines)
