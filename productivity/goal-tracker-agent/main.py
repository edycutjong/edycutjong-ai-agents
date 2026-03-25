#!/usr/bin/env python3
"""Goal Tracker Agent CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import create, progress, review, format_output

def cmd_create(args):
    inp = getattr(args, "create_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = create(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_progress(args):
    inp = getattr(args, "progress_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = progress(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_review(args):
    inp = getattr(args, "review_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = review(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Goal Tracker Agent")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create"); p.add_argument("create_input", nargs="?", default=""); p.set_defaults(func=cmd_create)
    p = sub.add_parser("progress"); p.add_argument("progress_input", nargs="?", default=""); p.set_defaults(func=cmd_progress)
    p = sub.add_parser("review"); p.add_argument("review_input", nargs="?", default=""); p.set_defaults(func=cmd_review)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
