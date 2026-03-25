#!/usr/bin/env python3
"""Documentation Quiz CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import quiz, score, export, format_output

def cmd_quiz(args):
    inp = getattr(args, "quiz_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = quiz(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_score(args):
    inp = getattr(args, "score_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = score(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_export(args):
    inp = getattr(args, "export_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = export(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Documentation Quiz")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("quiz"); p.add_argument("quiz_input", nargs="?", default=""); p.set_defaults(func=cmd_quiz)
    p = sub.add_parser("score"); p.add_argument("score_input", nargs="?", default=""); p.set_defaults(func=cmd_score)
    p = sub.add_parser("export"); p.add_argument("export_input", nargs="?", default=""); p.set_defaults(func=cmd_export)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
