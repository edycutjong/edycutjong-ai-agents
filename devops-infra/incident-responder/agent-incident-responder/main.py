#!/usr/bin/env python3
"""CLI for Incident Responder Agent.

Usage:
    python main.py monitor /var/log/app.log          # Watch log file
    python main.py diagnose /var/log/app.log          # One-shot diagnosis
    python main.py report incident-2024-01-15.json    # Generate post-mortem
"""
import argparse
import sys
import os
import json
import time
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from agent.detector import PatternDetector
from agent.diagnoser import Diagnoser
from agent.reporter import IncidentReporter


def main():
    parser = argparse.ArgumentParser(
        description="Incident Responder — AI-powered log monitoring & diagnosis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # monitor
    mon = subparsers.add_parser("monitor", help="Watch log files for issues")
    mon.add_argument("logfile", help="Path to log file")
    mon.add_argument("--rules", help="Custom rules YAML file")
    mon.add_argument("--interval", type=int, default=5, help="Check interval in seconds (default: 5)")
    mon.add_argument("--severity", choices=["info", "warn", "error", "critical"],
                     default="error", help="Minimum severity (default: error)")

    # diagnose
    diag = subparsers.add_parser("diagnose", help="One-shot log diagnosis")
    diag.add_argument("logfile", help="Path to log file")
    diag.add_argument("-n", "--lines", type=int, default=500, help="Lines to analyze (default: 500)")
    diag.add_argument("--format", choices=["text", "json", "markdown"], default="text")

    # report
    rep = subparsers.add_parser("report", help="Generate incident post-mortem")
    rep.add_argument("incident", help="Incident data file (JSON)")
    rep.add_argument("-o", "--output", help="Output file (default: stdout)")
    rep.add_argument("--template", choices=["standard", "brief", "detailed"],
                     default="standard", help="Report template")

    args = parser.parse_args()

    if args.command == "monitor":
        _monitor(args)
    elif args.command == "diagnose":
        _diagnose(args)
    elif args.command == "report":
        _report(args)


def _monitor(args):
    if not os.path.exists(args.logfile):
        print(f"Error: '{args.logfile}' not found.", file=sys.stderr)
        sys.exit(1)

    detector = PatternDetector(min_severity=args.severity)
    if args.rules:
        detector.load_rules(args.rules)

    print(f"🔍 Monitoring {args.logfile} (severity >= {args.severity})")
    print(f"   Press Ctrl+C to stop.\n")

    try:
        with open(args.logfile, "r") as f:
            # Seek to end
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    alerts = detector.check_line(line.strip())
                    for alert in alerts:
                        ts = datetime.now().strftime("%H:%M:%S")
                        icon = {"critical": "🔴", "error": "🟠", "warn": "🟡"}.get(alert.severity, "🔵")
                        print(f"  {icon} [{ts}] {alert.severity.upper()}: {alert.message}")
                        if alert.suggestion:
                            print(f"     💡 {alert.suggestion}")
                else:
                    time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\n✅ Monitoring stopped.")


def _diagnose(args):
    if not os.path.exists(args.logfile):
        print(f"Error: '{args.logfile}' not found.", file=sys.stderr)
        sys.exit(1)

    diagnoser = Diagnoser()

    print(f"🔬 Analyzing {args.logfile} (last {args.lines} lines)...")

    with open(args.logfile, "r") as f:
        lines = f.readlines()[-args.lines:]

    result = diagnoser.diagnose(lines)

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    elif args.format == "markdown":
        print(result.to_markdown())
    else:
        print(f"\n📊 Diagnosis Report")
        print(f"   Lines analyzed: {len(lines)}")
        print(f"   Issues found: {result.issue_count}")
        print(f"   Severity: {result.max_severity}")
        if result.patterns:
            print(f"\n🔍 Detected Patterns:")
            for p in result.patterns:
                print(f"   • {p}")
        if result.remediation:
            print(f"\n💡 Suggested Remediation:")
            for r in result.remediation:
                print(f"   → {r}")


def _report(args):
    if not os.path.exists(args.incident):
        print(f"Error: '{args.incident}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.incident, "r") as f:
        data = json.load(f)

    reporter = IncidentReporter(template=args.template)
    report = reporter.generate(data)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"✅ Report saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
