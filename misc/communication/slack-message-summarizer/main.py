#!/usr/bin/env python3
"""Slack Message Summarizer CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import summarize, digest, search, format_output

def cmd_summarize(args):
    inp = getattr(args, "summarize_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = summarize(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_digest(args):
    inp = getattr(args, "digest_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = digest(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_search(args):
    inp = getattr(args, "search_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = search(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Slack Message Summarizer")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("summarize"); p.add_argument("summarize_input", nargs="?", default=""); p.set_defaults(func=cmd_summarize)
    p = sub.add_parser("digest"); p.add_argument("digest_input", nargs="?", default=""); p.set_defaults(func=cmd_digest)
    p = sub.add_parser("search"); p.add_argument("search_input", nargs="?", default=""); p.set_defaults(func=cmd_search)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
