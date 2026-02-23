#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.summarizer import summarize, format_result_markdown
def cmd_summarize(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    r = summarize(text, ratio=args.ratio)
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Text Summarizer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("summarize"); a.add_argument("file", nargs="?", default="-"); a.add_argument("--ratio", type=float, default=0.3); a.set_defaults(func=cmd_summarize)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
