#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import parse_logs, analyze_logs, filter_by_level, format_analysis_markdown
def cmd_analyze(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    entries = parse_logs(text)
    if args.level: entries = filter_by_level(entries, args.level)
    a = analyze_logs(entries)
    print(format_analysis_markdown(a))
def main():
    p = argparse.ArgumentParser(description="Log Analyzer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("file", nargs="?", default="-"); a.add_argument("--level"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
