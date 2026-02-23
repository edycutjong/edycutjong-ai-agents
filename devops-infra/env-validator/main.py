#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.validator import parse_env, format_result_markdown
def cmd_validate(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    print(format_result_markdown(parse_env(text)))
def main():
    p = argparse.ArgumentParser(description="Env Validator"); s = p.add_subparsers(dest="command", required=True)
    v = s.add_parser("validate"); v.add_argument("file", nargs="?", default="-"); v.set_defaults(func=cmd_validate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
