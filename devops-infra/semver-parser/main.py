#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.parser import parse_semver, bump, format_result_markdown
def cmd_parse(args): print(format_result_markdown(parse_semver(args.version)))
def cmd_bump(args): print(format_result_markdown(bump(args.version, part=args.part)))
def main():
    p = argparse.ArgumentParser(description="SemVer Parser"); s = p.add_subparsers(dest="command", required=True)
    pa = s.add_parser("parse"); pa.add_argument("version"); pa.set_defaults(func=cmd_parse)
    b = s.add_parser("bump"); b.add_argument("version"); b.add_argument("--part", default="patch"); b.set_defaults(func=cmd_bump)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
