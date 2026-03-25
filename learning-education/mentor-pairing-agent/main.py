#!/usr/bin/env python3
"""Mentor Pairing Agent CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import assess, recommend, track, format_output

def cmd_assess(args):
    inp = getattr(args, "assess_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = assess(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_recommend(args):
    inp = getattr(args, "recommend_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = recommend(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_track(args):
    inp = getattr(args, "track_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = track(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Mentor Pairing Agent")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("assess"); p.add_argument("assess_input", nargs="?", default=""); p.set_defaults(func=cmd_assess)
    p = sub.add_parser("recommend"); p.add_argument("recommend_input", nargs="?", default=""); p.set_defaults(func=cmd_recommend)
    p = sub.add_parser("track"); p.add_argument("track_input", nargs="?", default=""); p.set_defaults(func=cmd_track)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
