"""Log diagnosis engine."""
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class DiagnosisResult:
    """Result of log analysis."""
    issue_count: int = 0
    max_severity: str = "info"
    patterns: List[str] = field(default_factory=list)
    remediation: List[str] = field(default_factory=list)
    error_summary: Dict[str, int] = field(default_factory=dict)
    timeline: List[Dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "issue_count": self.issue_count,
            "max_severity": self.max_severity,
            "patterns": self.patterns,
            "remediation": self.remediation,
            "error_summary": self.error_summary,
        }

    def to_markdown(self) -> str:
        lines = [
            "# Incident Diagnosis Report",
            "",
            f"**Issues found:** {self.issue_count}",
            f"**Max severity:** {self.max_severity}",
            "",
        ]
        if self.patterns:
            lines.append("## Detected Patterns")
            for p in self.patterns:
                lines.append(f"- {p}")
            lines.append("")
        if self.error_summary:
            lines.append("## Error Summary")
            lines.append("| Error Type | Count |")
            lines.append("|------------|-------|")
            for err, count in sorted(self.error_summary.items(), key=lambda x: -x[1]):
                lines.append(f"| {err} | {count} |")
            lines.append("")
        if self.remediation:
            lines.append("## Recommended Actions")
            for i, r in enumerate(self.remediation, 1):
                lines.append(f"{i}. {r}")
        return "\n".join(lines)


class Diagnoser:
    """Analyzes log files to diagnose issues."""

    ERROR_RE = re.compile(r"(ERROR|FATAL|CRITICAL|Exception|Traceback)", re.IGNORECASE)
    WARN_RE = re.compile(r"(WARN|WARNING)", re.IGNORECASE)
    TS_RE = re.compile(r"\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}")

    KNOWN_PATTERNS = {
        r"OutOfMemory|OOM|heap": ("Memory exhaustion", "Increase memory limits, check for leaks"),
        r"Connection refused|ECONNREFUSED": ("Connection failure", "Check target service health"),
        r"timeout|timed out": ("Timeout errors", "Review timeout configs, check network"),
        r"disk full|No space": ("Disk exhaustion", "Clean up disk, check log rotation"),
        r"deadlock": ("Database deadlock", "Review transaction isolation and ordering"),
        r"429|rate.?limit": ("Rate limiting", "Add backoff, reduce request frequency"),
        r"503|502|504": ("Service unavailability", "Check upstream health, review load balancer"),
        r"SIGKILL|killed": ("Process killed (OOM Killer?)", "Check memory limits and cgroup settings"),
    }

    def diagnose(self, lines: List[str]) -> DiagnosisResult:
        """Analyze log lines and produce diagnosis."""
        result = DiagnosisResult()
        error_types = Counter()
        severity_counts = Counter()

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if self.ERROR_RE.search(stripped):
                severity_counts["error"] += 1
                # Extract error type
                match = re.search(r"(\w+Error|\w+Exception)", stripped)
                if match:
                    error_types[match.group(1)] += 1
                else:
                    error_types["GenericError"] += 1

            elif self.WARN_RE.search(stripped):
                severity_counts["warn"] += 1

        result.issue_count = severity_counts.get("error", 0) + severity_counts.get("critical", 0)
        result.error_summary = dict(error_types.most_common(10))

        # Determine max severity
        all_text = "\n".join(lines)
        if re.search(r"CRITICAL|FATAL|OutOfMemory|segfault", all_text, re.IGNORECASE):
            result.max_severity = "critical"
        elif severity_counts.get("error", 0) > 0:
            result.max_severity = "error"
        elif severity_counts.get("warn", 0) > 0:
            result.max_severity = "warn"

        # Pattern matching
        for pattern, (name, remedy) in self.KNOWN_PATTERNS.items():
            if re.search(pattern, all_text, re.IGNORECASE):
                result.patterns.append(name)
                result.remediation.append(remedy)

        # Generic recommendations based on volume
        if result.issue_count > 100:
            result.remediation.append("High error volume — consider enabling circuit breakers")
        if len(error_types) > 5:
            result.remediation.append("Multiple error types — possible cascading failure")

        return result
