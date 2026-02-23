#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.converter import html_to_markdown, convert_file
def cmd_convert(args):
    if args.file == "-": html = sys.stdin.read()
    else: html = open(args.file).read()
    print(html_to_markdown(html))
def main():
    p = argparse.ArgumentParser(description="HTML to Markdown"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("convert"); c.add_argument("file", nargs="?", default="-"); c.set_defaults(func=cmd_convert)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
