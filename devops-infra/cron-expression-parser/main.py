#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.parser import parse_cron, format_result_markdown
def cmd_parse(args):
    r = parse_cron(args.expression)
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Cron Expression Parser"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("parse"); a.add_argument("expression"); a.set_defaults(func=cmd_parse)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
