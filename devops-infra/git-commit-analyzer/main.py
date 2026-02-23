#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import parse_commits, analyze_commits, format_analysis_markdown
def cmd_analyze(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    commits = parse_commits(text)
    a = analyze_commits(commits)
    print(format_analysis_markdown(a))
def main():
    p = argparse.ArgumentParser(description="Git Commit Analyzer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("file", nargs="?", default="-"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
