#!/usr/bin/env python3
"""Gas Fee Estimator CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import estimate, compare, optimal, format_output

def cmd_estimate(args):
    inp = getattr(args, "estimate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = estimate(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_compare(args):
    inp = getattr(args, "compare_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = compare(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_optimal(args):
    inp = getattr(args, "optimal_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = optimal(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Gas Fee Estimator")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("estimate"); p.add_argument("estimate_input", nargs="?", default=""); p.set_defaults(func=cmd_estimate)
    p = sub.add_parser("compare"); p.add_argument("compare_input", nargs="?", default=""); p.set_defaults(func=cmd_compare)
    p = sub.add_parser("optimal"); p.add_argument("optimal_input", nargs="?", default=""); p.set_defaults(func=cmd_optimal)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
