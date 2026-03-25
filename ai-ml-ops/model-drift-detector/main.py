#!/usr/bin/env python3
"""Model Drift Detector CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import detect, compare, alert, format_output

def cmd_detect(args):
    inp = getattr(args, "detect_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = detect(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_compare(args):
    inp = getattr(args, "compare_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = compare(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_alert(args):
    inp = getattr(args, "alert_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = alert(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Model Drift Detector")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("detect"); p.add_argument("detect_input", nargs="?", default=""); p.set_defaults(func=cmd_detect)
    p = sub.add_parser("compare"); p.add_argument("compare_input", nargs="?", default=""); p.set_defaults(func=cmd_compare)
    p = sub.add_parser("alert"); p.add_argument("alert_input", nargs="?", default=""); p.set_defaults(func=cmd_alert)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
