#!/usr/bin/env python3
"""CLI for API Changelog Differ."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.differ import diff_specs, format_diff_markdown

def cmd_diff(args):
    old = json.load(open(args.old))
    new = json.load(open(args.new))
    result = diff_specs(old, new)
    if args.json: print(json.dumps(result.to_dict(), indent=2))
    else: print(format_diff_markdown(result))
    if result.breaking_count > 0 and args.fail_on_breaking: sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="API Changelog Differ")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("diff"); p.add_argument("old"); p.add_argument("new"); p.add_argument("--json", action="store_true"); p.add_argument("--fail-on-breaking", action="store_true"); p.set_defaults(func=cmd_diff)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
