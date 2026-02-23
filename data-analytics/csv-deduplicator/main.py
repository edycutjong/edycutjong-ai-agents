#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.deduplicator import parse_csv, deduplicate, to_csv_string, format_result_markdown
def cmd_dedupe(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    headers, rows = parse_csv(text)
    unique, result = deduplicate(headers, rows)
    if args.report: print(format_result_markdown(result))
    else: print(to_csv_string(headers, unique))
def main():
    p = argparse.ArgumentParser(description="CSV Deduplicator"); s = p.add_subparsers(dest="command", required=True)
    d = s.add_parser("dedupe"); d.add_argument("file", nargs="?", default="-"); d.add_argument("--report", action="store_true"); d.set_defaults(func=cmd_dedupe)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
