#!/usr/bin/env python3
"""Pomodoro Coach CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import start, stats, tips, format_output

def cmd_start(args):
    inp = getattr(args, "start_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = start(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_stats(args):
    inp = getattr(args, "stats_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = stats(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_tips(args):
    inp = getattr(args, "tips_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = tips(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Pomodoro Coach")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start"); p.add_argument("start_input", nargs="?", default=""); p.set_defaults(func=cmd_start)
    p = sub.add_parser("stats"); p.add_argument("stats_input", nargs="?", default=""); p.set_defaults(func=cmd_stats)
    p = sub.add_parser("tips"); p.add_argument("tips_input", nargs="?", default=""); p.set_defaults(func=cmd_tips)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
