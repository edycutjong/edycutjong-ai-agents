#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_types
def cmd_generate(args):
    data = sys.stdin.read() if args.file == "-" else open(args.file).read()
    print(generate_types(data, name=args.name, fmt=args.format))
def main():
    p = argparse.ArgumentParser(description="Type Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("file"); g.add_argument("--name", default="Root"); g.add_argument("--format", default="typescript", choices=["typescript","python","zod"]); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
