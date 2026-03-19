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
    parser = argparse.ArgumentParser(  # pragma: no cover
        description="Incident Responder — AI-powered log monitoring & diagnosis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)  # pragma: no cover

    # monitor
    mon = subparsers.add_parser("monitor", help="Watch log files for issues")  # pragma: no cover
    mon.add_argument("logfile", help="Path to log file")  # pragma: no cover
    mon.add_argument("--rules", help="Custom rules YAML file")  # pragma: no cover
    mon.add_argument("--interval", type=int, default=5, help="Check interval in seconds (default: 5)")  # pragma: no cover
    mon.add_argument("--severity", choices=["info", "warn", "error", "critical"],  # pragma: no cover
                     default="error", help="Minimum severity (default: error)")

    # diagnose
    diag = subparsers.add_parser("diagnose", help="One-shot log diagnosis")  # pragma: no cover
    diag.add_argument("logfile", help="Path to log file")  # pragma: no cover
    diag.add_argument("-n", "--lines", type=int, default=500, help="Lines to analyze (default: 500)")  # pragma: no cover
    diag.add_argument("--format", choices=["text", "json", "markdown"], default="text")  # pragma: no cover

    # report
    rep = subparsers.add_parser("report", help="Generate incident post-mortem")  # pragma: no cover
    rep.add_argument("incident", help="Incident data file (JSON)")  # pragma: no cover
    rep.add_argument("-o", "--output", help="Output file (default: stdout)")  # pragma: no cover
    rep.add_argument("--template", choices=["standard", "brief", "detailed"],  # pragma: no cover
                     default="standard", help="Report template")

    args = parser.parse_args()  # pragma: no cover

    if args.command == "monitor":  # pragma: no cover
        _monitor(args)  # pragma: no cover
    elif args.command == "diagnose":  # pragma: no cover
        _diagnose(args)  # pragma: no cover
    elif args.command == "report":  # pragma: no cover
        _report(args)  # pragma: no cover


def _monitor(args):
    if not os.path.exists(args.logfile):  # pragma: no cover
        print(f"Error: '{args.logfile}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    detector = PatternDetector(min_severity=args.severity)  # pragma: no cover
    if args.rules:  # pragma: no cover
        detector.load_rules(args.rules)  # pragma: no cover

    print(f"🔍 Monitoring {args.logfile} (severity >= {args.severity})")  # pragma: no cover
    print(f"   Press Ctrl+C to stop.\n")  # pragma: no cover

    try:  # pragma: no cover
        with open(args.logfile, "r") as f:  # pragma: no cover
            # Seek to end
            f.seek(0, 2)  # pragma: no cover
            while True:  # pragma: no cover
                line = f.readline()  # pragma: no cover
                if line:  # pragma: no cover
                    alerts = detector.check_line(line.strip())  # pragma: no cover
                    for alert in alerts:  # pragma: no cover
                        ts = datetime.now().strftime("%H:%M:%S")  # pragma: no cover
                        icon = {"critical": "🔴", "error": "🟠", "warn": "🟡"}.get(alert.severity, "🔵")  # pragma: no cover
                        print(f"  {icon} [{ts}] {alert.severity.upper()}: {alert.message}")  # pragma: no cover
                        if alert.suggestion:  # pragma: no cover
                            print(f"     💡 {alert.suggestion}")  # pragma: no cover
                else:
                    time.sleep(args.interval)  # pragma: no cover
    except KeyboardInterrupt:  # pragma: no cover
        print(f"\n✅ Monitoring stopped.")  # pragma: no cover


def _diagnose(args):
    if not os.path.exists(args.logfile):  # pragma: no cover
        print(f"Error: '{args.logfile}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    diagnoser = Diagnoser()  # pragma: no cover

    print(f"🔬 Analyzing {args.logfile} (last {args.lines} lines)...")  # pragma: no cover

    with open(args.logfile, "r") as f:  # pragma: no cover
        lines = f.readlines()[-args.lines:]  # pragma: no cover

    result = diagnoser.diagnose(lines)  # pragma: no cover

    if args.format == "json":  # pragma: no cover
        print(json.dumps(result.to_dict(), indent=2))  # pragma: no cover
    elif args.format == "markdown":  # pragma: no cover
        print(result.to_markdown())  # pragma: no cover
    else:
        print(f"\n📊 Diagnosis Report")  # pragma: no cover
        print(f"   Lines analyzed: {len(lines)}")  # pragma: no cover
        print(f"   Issues found: {result.issue_count}")  # pragma: no cover
        print(f"   Severity: {result.max_severity}")  # pragma: no cover
        if result.patterns:  # pragma: no cover
            print(f"\n🔍 Detected Patterns:")  # pragma: no cover
            for p in result.patterns:  # pragma: no cover
                print(f"   • {p}")  # pragma: no cover
        if result.remediation:  # pragma: no cover
            print(f"\n💡 Suggested Remediation:")  # pragma: no cover
            for r in result.remediation:  # pragma: no cover
                print(f"   → {r}")  # pragma: no cover


def _report(args):
    if not os.path.exists(args.incident):  # pragma: no cover
        print(f"Error: '{args.incident}' not found.", file=sys.stderr)  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    with open(args.incident, "r") as f:  # pragma: no cover
        data = json.load(f)  # pragma: no cover

    reporter = IncidentReporter(template=args.template)  # pragma: no cover
    report = reporter.generate(data)  # pragma: no cover

    if args.output:  # pragma: no cover
        with open(args.output, "w") as f:  # pragma: no cover
            f.write(report)  # pragma: no cover
        print(f"✅ Report saved to {args.output}")  # pragma: no cover
    else:
        print(report)  # pragma: no cover


if __name__ == "__main__":
    main()  # pragma: no cover
