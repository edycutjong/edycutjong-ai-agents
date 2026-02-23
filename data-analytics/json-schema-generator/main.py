#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_from_json, format_schema
def cmd_generate(args):
    data = sys.stdin.read() if args.file == "-" else open(args.file).read()
    schema = generate_from_json(data, title=args.title)
    print(format_schema(schema))
def main():
    p = argparse.ArgumentParser(description="JSON Schema Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("file", nargs="?", default="-"); g.add_argument("--title", default="Root"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
