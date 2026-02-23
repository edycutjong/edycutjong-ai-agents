#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.formatter import format_json, format_result_markdown
def cmd_format(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    r = format_json(text, indent=args.indent, sort_keys=args.sort)
    print(r.formatted if r.is_valid else f"Error: {r.error}")
def main():
    p = argparse.ArgumentParser(description="JSON Formatter"); s = p.add_subparsers(dest="command", required=True)
    f = s.add_parser("format"); f.add_argument("file", nargs="?", default="-"); f.add_argument("--indent", type=int, default=2); f.add_argument("--sort", action="store_true"); f.set_defaults(func=cmd_format)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
