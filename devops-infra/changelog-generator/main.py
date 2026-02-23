#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_changelog, format_changelog_markdown
def cmd_generate(args):
    messages = sys.stdin.read().strip().split("\n") if args.file == "-" else open(args.file).read().strip().split("\n")
    r = generate_changelog(messages, version=args.version)
    print(format_changelog_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Changelog Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("file", nargs="?", default="-"); g.add_argument("--version", default="Unreleased"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
