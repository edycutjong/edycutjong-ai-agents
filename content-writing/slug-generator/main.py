#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import slugify, format_result_markdown
def cmd_generate(args): print(format_result_markdown(slugify(args.text, separator=args.sep, max_length=args.max_length)))
def main():
    p = argparse.ArgumentParser(description="Slug Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("text"); g.add_argument("--sep", default="-"); g.add_argument("--max-length", type=int, default=0); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
