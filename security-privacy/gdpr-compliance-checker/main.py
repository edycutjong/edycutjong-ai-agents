#!/usr/bin/env python3
"""GDPR Compliance Checker CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import check, scan, report, format_output

def cmd_check(args):
    inp = getattr(args, "check_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = check(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_scan(args):
    inp = getattr(args, "scan_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = scan(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_report(args):
    inp = getattr(args, "report_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = report(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="GDPR Compliance Checker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check"); p.add_argument("check_input", nargs="?", default=""); p.set_defaults(func=cmd_check)
    p = sub.add_parser("scan"); p.add_argument("scan_input", nargs="?", default=""); p.set_defaults(func=cmd_scan)
    p = sub.add_parser("report"); p.add_argument("report_input", nargs="?", default=""); p.set_defaults(func=cmd_report)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
