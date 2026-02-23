#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.validator import parse_cors_config, validate_cors, format_result_markdown
def cmd_validate(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    config = parse_cors_config(json.loads(text))
    result = validate_cors(config)
    print(format_result_markdown(config, result))
def main():
    p = argparse.ArgumentParser(description="CORS Config Validator"); s = p.add_subparsers(dest="command", required=True)
    v = s.add_parser("validate"); v.add_argument("file", nargs="?", default="-"); v.set_defaults(func=cmd_validate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
