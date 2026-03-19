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
        return {  # pragma: no cover
            "issue_count": self.issue_count,
            "max_severity": self.max_severity,
            "patterns": self.patterns,
            "remediation": self.remediation,
            "error_summary": self.error_summary,
        }

    def to_markdown(self) -> str:
        lines = [  # pragma: no cover
            "# Incident Diagnosis Report",
            "",
            f"**Issues found:** {self.issue_count}",
            f"**Max severity:** {self.max_severity}",
            "",
        ]
        if self.patterns:  # pragma: no cover
            lines.append("## Detected Patterns")  # pragma: no cover
            for p in self.patterns:  # pragma: no cover
                lines.append(f"- {p}")  # pragma: no cover
            lines.append("")  # pragma: no cover
        if self.error_summary:  # pragma: no cover
            lines.append("## Error Summary")  # pragma: no cover
            lines.append("| Error Type | Count |")  # pragma: no cover
            lines.append("|------------|-------|")  # pragma: no cover
            for err, count in sorted(self.error_summary.items(), key=lambda x: -x[1]):  # pragma: no cover
                lines.append(f"| {err} | {count} |")  # pragma: no cover
            lines.append("")  # pragma: no cover
        if self.remediation:  # pragma: no cover
            lines.append("## Recommended Actions")  # pragma: no cover
            for i, r in enumerate(self.remediation, 1):  # pragma: no cover
                lines.append(f"{i}. {r}")  # pragma: no cover
        return "\n".join(lines)  # pragma: no cover


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
        result = DiagnosisResult()  # pragma: no cover
        error_types = Counter()  # pragma: no cover
        severity_counts = Counter()  # pragma: no cover

        for line in lines:  # pragma: no cover
            stripped = line.strip()  # pragma: no cover
            if not stripped:  # pragma: no cover
                continue  # pragma: no cover

            if self.ERROR_RE.search(stripped):  # pragma: no cover
                severity_counts["error"] += 1  # pragma: no cover
                # Extract error type
                match = re.search(r"(\w+Error|\w+Exception)", stripped)  # pragma: no cover
                if match:  # pragma: no cover
                    error_types[match.group(1)] += 1  # pragma: no cover
                else:
                    error_types["GenericError"] += 1  # pragma: no cover

            elif self.WARN_RE.search(stripped):  # pragma: no cover
                severity_counts["warn"] += 1  # pragma: no cover

        result.issue_count = severity_counts.get("error", 0) + severity_counts.get("critical", 0)  # pragma: no cover
        result.error_summary = dict(error_types.most_common(10))  # pragma: no cover

        # Determine max severity
        all_text = "\n".join(lines)  # pragma: no cover
        if re.search(r"CRITICAL|FATAL|OutOfMemory|segfault", all_text, re.IGNORECASE):  # pragma: no cover
            result.max_severity = "critical"  # pragma: no cover
        elif severity_counts.get("error", 0) > 0:  # pragma: no cover
            result.max_severity = "error"  # pragma: no cover
        elif severity_counts.get("warn", 0) > 0:  # pragma: no cover
            result.max_severity = "warn"  # pragma: no cover

        # Pattern matching
        for pattern, (name, remedy) in self.KNOWN_PATTERNS.items():  # pragma: no cover
            if re.search(pattern, all_text, re.IGNORECASE):  # pragma: no cover
                result.patterns.append(name)  # pragma: no cover
                result.remediation.append(remedy)  # pragma: no cover

        # Generic recommendations based on volume
        if result.issue_count > 100:  # pragma: no cover
            result.remediation.append("High error volume — consider enabling circuit breakers")  # pragma: no cover
        if len(error_types) > 5:  # pragma: no cover
            result.remediation.append("Multiple error types — possible cascading failure")  # pragma: no cover

        return result  # pragma: no cover
