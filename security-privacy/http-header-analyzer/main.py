#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import analyze_headers, format_result_markdown
def cmd_analyze(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    r = analyze_headers(json.loads(text))
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="HTTP Header Analyzer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("file", nargs="?", default="-"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
