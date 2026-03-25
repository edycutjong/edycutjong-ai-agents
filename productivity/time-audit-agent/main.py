#!/usr/bin/env python3
"""Time Audit Agent CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import audit, analyze, optimize, format_output

def cmd_audit(args):
    inp = getattr(args, "audit_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = audit(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_analyze(args):
    inp = getattr(args, "analyze_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = analyze(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_optimize(args):
    inp = getattr(args, "optimize_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = optimize(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Time Audit Agent")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("audit"); p.add_argument("audit_input", nargs="?", default=""); p.set_defaults(func=cmd_audit)
    p = sub.add_parser("analyze"); p.add_argument("analyze_input", nargs="?", default=""); p.set_defaults(func=cmd_analyze)
    p = sub.add_parser("optimize"); p.add_argument("optimize_input", nargs="?", default=""); p.set_defaults(func=cmd_optimize)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
