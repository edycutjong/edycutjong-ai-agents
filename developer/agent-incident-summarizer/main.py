"""
Incident Summarizer Agent — parses logs and error reports to generate incident summaries.
Usage: python main.py <logfile>
"""
import argparse
import os
import re
import sys
from collections import Counter
from datetime import datetime


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Incident Summarizer] Provide log output or error reports to generate an incident summary."


ERROR_PATTERNS = [
    (r"(?i)\b(error|exception|fatal|critical|panic)\b", "ERROR"),
    (r"(?i)\b(warn|warning)\b", "WARNING"),
    (r"(?i)\b(timeout|timed?\s*out)\b", "TIMEOUT"),
    (r"(?i)\b(connection\s+refused|ECONNREFUSED)\b", "CONN_REFUSED"),
    (r"(?i)\b(out\s+of\s+memory|OOM|MemoryError)\b", "OOM"),
    (r"(?i)\b(5\d{2})\b", "HTTP_5XX"),
    (r"(?i)\b(4\d{2})\b", "HTTP_4XX"),
    (r"(?i)\b(segfault|segmentation\s+fault)\b", "SEGFAULT"),
]

TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}")


def extract_events(content: str) -> list:
    events = []
    for i, line in enumerate(content.splitlines(), 1):
        for pattern, category in ERROR_PATTERNS:
            if re.search(pattern, line):
                ts_match = TIMESTAMP_RE.search(line)
                events.append({
                    "line": i, "category": category,
                    "timestamp": ts_match.group() if ts_match else None,
                    "content": line.strip()[:120]
                })
                break
    return events


def classify_severity(events: list) -> str:
    categories = [e["category"] for e in events]
    if any(c in categories for c in ["OOM", "SEGFAULT"]):
        return "CRITICAL"
    if any(c in categories for c in ["CONN_REFUSED", "TIMEOUT"]):
        return "HIGH"
    error_count = sum(1 for c in categories if c == "ERROR")
    if error_count > 10:
        return "HIGH"
    if error_count > 0:
        return "MEDIUM"
    return "LOW"


def generate_summary(events: list, filename: str = "") -> str:
    if not events:
        return "✅ No incidents detected in the log."
    cat_counts = Counter(e["category"] for e in events)
    severity = classify_severity(events)
    icons = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}
    lines = [f"📋 Incident Summary {f'— {filename}' if filename else ''}",
             f"  Severity: {icons.get(severity, '⚪')} {severity}",
             f"  Total events: {len(events)}\n",
             "  Breakdown:"]
    for cat, count in cat_counts.most_common():
        lines.append(f"    - {cat}: {count}")
    lines.append("\n  Sample events:")
    for e in events[:5]:
        ts = f"[{e['timestamp']}] " if e["timestamp"] else ""
        lines.append(f"    L{e['line']}: {ts}{e['content'][:80]}")
    if len(events) > 5:
        lines.append(f"    ... and {len(events) - 5} more")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Incident Summarizer Agent")
    parser.add_argument("file", nargs="?", help="Log file to analyze")
    args = parser.parse_args()
    if not args.file:
        print("Incident Summarizer Agent\nUsage: python main.py <logfile>")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"Error: {args.file} not found")
        sys.exit(1)
    content = open(args.file).read()
    events = extract_events(content)
    print(generate_summary(events, args.file))


if __name__ == "__main__":
    main()
