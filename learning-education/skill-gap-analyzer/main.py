#!/usr/bin/env python3
"""Skill Gap Analyzer CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import analyze, match, report, format_output

def cmd_analyze(args):
    inp = getattr(args, "analyze_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = analyze(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_match(args):
    inp = getattr(args, "match_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = match(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_report(args):
    inp = getattr(args, "report_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = report(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Skill Gap Analyzer")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze"); p.add_argument("analyze_input", nargs="?", default=""); p.set_defaults(func=cmd_analyze)
    p = sub.add_parser("match"); p.add_argument("match_input", nargs="?", default=""); p.set_defaults(func=cmd_match)
    p = sub.add_parser("report"); p.add_argument("report_input", nargs="?", default=""); p.set_defaults(func=cmd_report)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
