#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.counter import count_words, format_result_markdown
def cmd_count(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    print(format_result_markdown(count_words(text)))
def main():
    p = argparse.ArgumentParser(description="Word Counter"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("count"); c.add_argument("file", nargs="?", default="-"); c.set_defaults(func=cmd_count)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
