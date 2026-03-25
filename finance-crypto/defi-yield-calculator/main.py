#!/usr/bin/env python3
"""DeFi Yield Calculator CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import calculate, compare, risk, format_output

def cmd_calculate(args):
    inp = getattr(args, "calculate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = calculate(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_compare(args):
    inp = getattr(args, "compare_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = compare(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_risk(args):
    inp = getattr(args, "risk_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = risk(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="DeFi Yield Calculator")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("calculate"); p.add_argument("calculate_input", nargs="?", default=""); p.set_defaults(func=cmd_calculate)
    p = sub.add_parser("compare"); p.add_argument("compare_input", nargs="?", default=""); p.set_defaults(func=cmd_compare)
    p = sub.add_parser("risk"); p.add_argument("risk_input", nargs="?", default=""); p.set_defaults(func=cmd_risk)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
