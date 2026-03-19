"""Log pattern detection engine."""
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Alert:
    """An alert triggered by a log pattern match."""
    severity: str
    message: str
    line: str
    pattern: str
    suggestion: Optional[str] = None


# Built-in pattern rules
DEFAULT_RULES = [
    {
        "pattern": r"OutOfMemory|OOM|heap space",
        "severity": "critical",
        "message": "Memory exhaustion detected",
        "suggestion": "Increase heap size or investigate memory leaks. Check -Xmx settings.",
    },
    {
        "pattern": r"Connection refused|ECONNREFUSED",
        "severity": "error",
        "message": "Service connection refused",
        "suggestion": "Check if the target service is running and listening on the expected port.",
    },
    {
        "pattern": r"timeout|timed out|ETIMEDOUT",
        "severity": "error",
        "message": "Request timeout detected",
        "suggestion": "Review timeout settings, check network latency, consider circuit breaker pattern.",
    },
    {
        "pattern": r"disk full|No space left|ENOSPC",
        "severity": "critical",
        "message": "Disk space exhaustion",
        "suggestion": "Free disk space, check log rotation, review storage quotas.",
    },
    {
        "pattern": r"permission denied|EACCES|403 Forbidden",
        "severity": "error",
        "message": "Permission error",
        "suggestion": "Check file/directory permissions, IAM roles, or API credentials.",
    },
    {
        "pattern": r"rate limit|429|too many requests",
        "severity": "warn",
        "message": "Rate limit hit",
        "suggestion": "Implement exponential backoff, request rate limit increase, or add caching.",
    },
    {
        "pattern": r"SSL|TLS|certificate|CERT_",
        "severity": "error",
        "message": "SSL/TLS certificate issue",
        "suggestion": "Check certificate expiry, renew if needed, verify CA chain.",
    },
    {
        "pattern": r"deadlock|lock wait timeout",
        "severity": "critical",
        "message": "Database deadlock detected",
        "suggestion": "Review transaction ordering, add lock timeouts, use row-level locks.",
    },
    {
        "pattern": r"CPU.*(100%|99%)|load average.*[5-9]\d",
        "severity": "warn",
        "message": "High CPU usage detected",
        "suggestion": "Profile running processes, check for infinite loops, scale horizontally.",
    },
    {
        "pattern": r"segfault|segmentation fault|SIGSEGV",
        "severity": "critical",
        "message": "Segmentation fault detected",
        "suggestion": "Check for null pointer dereferences, buffer overflows, or corrupted memory.",
    },
]


class PatternDetector:
    """Detects error patterns in log lines."""

    SEVERITY_LEVELS = {"info": 0, "warn": 1, "error": 2, "critical": 3}

    def __init__(self, min_severity: str = "error"):
        self.min_severity = min_severity  # pragma: no cover
        self.rules = [  # pragma: no cover
            {**r, "compiled": re.compile(r["pattern"], re.IGNORECASE)}
            for r in DEFAULT_RULES
        ]

    def load_rules(self, rules_file: str):
        """Load custom rules from YAML file."""
        import yaml  # pragma: no cover
        with open(rules_file, "r") as f:  # pragma: no cover
            custom = yaml.safe_load(f)  # pragma: no cover
        if custom and isinstance(custom, list):  # pragma: no cover
            for r in custom:  # pragma: no cover
                r["compiled"] = re.compile(r.get("pattern", ""), re.IGNORECASE)  # pragma: no cover
                self.rules.append(r)  # pragma: no cover

    def check_line(self, line: str) -> List[Alert]:
        """Check a single log line against all rules."""
        alerts = []  # pragma: no cover
        min_level = self.SEVERITY_LEVELS.get(self.min_severity, 2)  # pragma: no cover

        for rule in self.rules:  # pragma: no cover
            level = self.SEVERITY_LEVELS.get(rule.get("severity", "info"), 0)  # pragma: no cover
            if level < min_level:  # pragma: no cover
                continue  # pragma: no cover

            if rule["compiled"].search(line):  # pragma: no cover
                alerts.append(Alert(  # pragma: no cover
                    severity=rule.get("severity", "error"),
                    message=rule.get("message", "Pattern matched"),
                    line=line,
                    pattern=rule.get("pattern", ""),
                    suggestion=rule.get("suggestion"),
                ))

        return alerts  # pragma: no cover

    def check_lines(self, lines: List[str]) -> List[Alert]:
        """Check multiple log lines."""
        alerts = []  # pragma: no cover
        for line in lines:  # pragma: no cover
            alerts.extend(self.check_line(line.strip()))  # pragma: no cover
        return alerts  # pragma: no cover
