#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import detect_framework, PARSERS, generate_openapi, generate_markdown_docs
def cmd_generate(args):
    code = open(args.file).read()
    fw = args.framework or detect_framework(code)
    endpoints = PARSERS.get(fw, PARSERS["flask"])(code)
    if args.format == "openapi": print(json.dumps(generate_openapi(endpoints, title=args.title), indent=2))
    else: print(generate_markdown_docs(endpoints, title=args.title))
def main():
    p = argparse.ArgumentParser(description="API Doc Generator")
    s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("file"); g.add_argument("--framework", choices=["flask","express","fastapi"]); g.add_argument("--format", default="markdown", choices=["markdown","openapi"]); g.add_argument("--title", default="API"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
