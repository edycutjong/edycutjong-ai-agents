#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.builder import run_test, get_pattern, list_patterns, explain_pattern, format_test_markdown
def cmd_test(args):
    text = sys.stdin.read() if args.text == "-" else args.text
    r = run_test(args.pattern, text)
    print(format_test_markdown(r))
def cmd_list(args):
    for p in list_patterns(): print(f"  {p}: {get_pattern(p)}")
def cmd_explain(args):
    print(explain_pattern(args.pattern))
def main():
    p = argparse.ArgumentParser(description="Regex Builder"); s = p.add_subparsers(dest="command", required=True)
    t = s.add_parser("test"); t.add_argument("pattern"); t.add_argument("text", nargs="?", default="-"); t.set_defaults(func=cmd_test)
    l = s.add_parser("list"); l.set_defaults(func=cmd_list)
    e = s.add_parser("explain"); e.add_argument("pattern"); e.set_defaults(func=cmd_explain)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
