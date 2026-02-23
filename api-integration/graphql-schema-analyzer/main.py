#!/usr/bin/env python3
"""CLI for GraphQL Schema Analyzer."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import parse_schema, get_schema_stats, format_analysis_markdown, find_unused_types, find_complexity_issues

def cmd_analyze(args):
    sdl = sys.stdin.read() if args.file == "-" else open(args.file).read()
    types = parse_schema(sdl)
    stats = get_schema_stats(types)
    if args.json:
        print(json.dumps({"stats": stats.to_dict(), "types": [t.to_dict() for t in types], "unused": find_unused_types(types), "issues": find_complexity_issues(types)}, indent=2))
    else:
        print(format_analysis_markdown(types, stats))

def main():
    parser = argparse.ArgumentParser(description="GraphQL Schema Analyzer")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze"); p.add_argument("file"); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_analyze)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
