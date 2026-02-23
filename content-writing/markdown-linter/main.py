#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.linter import lint_markdown, format_result_markdown
def cmd_lint(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    print(format_result_markdown(lint_markdown(text)))
def main():
    p = argparse.ArgumentParser(description="Markdown Linter"); s = p.add_subparsers(dest="command", required=True)
    l = s.add_parser("lint"); l.add_argument("file", nargs="?", default="-"); l.set_defaults(func=cmd_lint)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
