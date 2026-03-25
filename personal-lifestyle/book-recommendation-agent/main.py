#!/usr/bin/env python3
"""Book Recommendation Agent CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import recommend, search, list, format_output

def cmd_recommend(args):
    inp = getattr(args, "recommend_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = recommend(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_search(args):
    inp = getattr(args, "search_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = search(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_list(args):
    inp = getattr(args, "list_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = list(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Book Recommendation Agent")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("recommend"); p.add_argument("recommend_input", nargs="?", default=""); p.set_defaults(func=cmd_recommend)
    p = sub.add_parser("search"); p.add_argument("search_input", nargs="?", default=""); p.set_defaults(func=cmd_search)
    p = sub.add_parser("list"); p.add_argument("list_input", nargs="?", default=""); p.set_defaults(func=cmd_list)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
