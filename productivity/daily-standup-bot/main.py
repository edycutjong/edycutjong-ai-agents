#!/usr/bin/env python3
"""Daily Standup Bot CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import collect, summarize, archive, format_output

def cmd_collect(args):
    inp = getattr(args, "collect_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = collect(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_summarize(args):
    inp = getattr(args, "summarize_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = summarize(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_archive(args):
    inp = getattr(args, "archive_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = archive(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Daily Standup Bot")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("collect"); p.add_argument("collect_input", nargs="?", default=""); p.set_defaults(func=cmd_collect)
    p = sub.add_parser("summarize"); p.add_argument("summarize_input", nargs="?", default=""); p.set_defaults(func=cmd_summarize)
    p = sub.add_parser("archive"); p.add_argument("archive_input", nargs="?", default=""); p.set_defaults(func=cmd_archive)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
