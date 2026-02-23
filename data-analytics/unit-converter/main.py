#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.converter import convert, format_result_markdown
def cmd_convert(args): print(format_result_markdown(convert(args.value, args.from_unit, args.to_unit)))
def main():
    p = argparse.ArgumentParser(description="Unit Converter"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("convert"); c.add_argument("value", type=float); c.add_argument("from_unit"); c.add_argument("to_unit"); c.set_defaults(func=cmd_convert)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
