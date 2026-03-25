#!/usr/bin/env python3
"""LLM Prompt Tester CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import test, compare, best, format_output

def cmd_test(args):
    inp = getattr(args, "test_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = test(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_compare(args):
    inp = getattr(args, "compare_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = compare(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_best(args):
    inp = getattr(args, "best_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = best(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="LLM Prompt Tester")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("test"); p.add_argument("test_input", nargs="?", default=""); p.set_defaults(func=cmd_test)
    p = sub.add_parser("compare"); p.add_argument("compare_input", nargs="?", default=""); p.set_defaults(func=cmd_compare)
    p = sub.add_parser("best"); p.add_argument("best_input", nargs="?", default=""); p.set_defaults(func=cmd_best)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
