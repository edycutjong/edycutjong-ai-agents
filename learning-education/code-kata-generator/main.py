#!/usr/bin/env python3
"""Code Kata Generator CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import generate, grade, hint, format_output

def cmd_generate(args):
    inp = getattr(args, "generate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = generate(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_grade(args):
    inp = getattr(args, "grade_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = grade(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_hint(args):
    inp = getattr(args, "hint_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = hint(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Code Kata Generator")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate"); p.add_argument("generate_input", nargs="?", default=""); p.set_defaults(func=cmd_generate)
    p = sub.add_parser("grade"); p.add_argument("grade_input", nargs="?", default=""); p.set_defaults(func=cmd_grade)
    p = sub.add_parser("hint"); p.add_argument("hint_input", nargs="?", default=""); p.set_defaults(func=cmd_hint)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
