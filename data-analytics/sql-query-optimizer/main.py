#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.optimizer import analyze_query, format_analysis_markdown
def cmd_analyze(args):
    q = sys.stdin.read() if args.query == "-" else args.query
    a = analyze_query(q)
    print(format_analysis_markdown(a))
def main():
    p = argparse.ArgumentParser(description="SQL Query Optimizer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("query", nargs="?", default="-"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
