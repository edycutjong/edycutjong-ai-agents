#!/usr/bin/env python3
"""Budget Tracker Agent CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import import_data, categorize, report, format_output

def cmd_import_data(args):
    inp = getattr(args, "import_data_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = import_data(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_categorize(args):
    inp = getattr(args, "categorize_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = categorize(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_report(args):
    inp = getattr(args, "report_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = report(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Budget Tracker Agent")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("import_data"); p.add_argument("import_data_input", nargs="?", default=""); p.set_defaults(func=cmd_import_data)
    p = sub.add_parser("categorize"); p.add_argument("categorize_input", nargs="?", default=""); p.set_defaults(func=cmd_categorize)
    p = sub.add_parser("report"); p.add_argument("report_input", nargs="?", default=""); p.set_defaults(func=cmd_report)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
