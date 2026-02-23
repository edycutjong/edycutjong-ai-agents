#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.explainer import explain_code
def cmd_explain(args):
    code = sys.stdin.read() if args.file == "-" else open(args.file).read()
    print(explain_code(code, language=args.language))
def main():
    p = argparse.ArgumentParser(description="Code Explainer"); s = p.add_subparsers(dest="command", required=True)
    e = s.add_parser("explain"); e.add_argument("file", nargs="?", default="-"); e.add_argument("--language"); e.set_defaults(func=cmd_explain)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
