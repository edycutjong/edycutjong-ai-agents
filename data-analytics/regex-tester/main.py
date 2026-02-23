#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.tester import run_regex_test, format_result_markdown
def cmd_test(args): print(format_result_markdown(run_regex_test(args.pattern, args.text, flags=args.flags or "")))
def main():
    p = argparse.ArgumentParser(description="Regex Tester"); s = p.add_subparsers(dest="command", required=True)
    t = s.add_parser("test"); t.add_argument("pattern"); t.add_argument("text"); t.add_argument("--flags", default=""); t.set_defaults(func=cmd_test)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
