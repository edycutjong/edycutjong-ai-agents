#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.validator import validate_response, create_rules_from_sample, format_result_markdown
def cmd_validate(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    data = json.loads(text)
    rules = create_rules_from_sample(data)
    r = validate_response(data, rules, status_code=args.status)
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="API Response Validator"); s = p.add_subparsers(dest="command", required=True)
    v = s.add_parser("validate"); v.add_argument("file", nargs="?", default="-"); v.add_argument("--status", type=int, default=200); v.set_defaults(func=cmd_validate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
