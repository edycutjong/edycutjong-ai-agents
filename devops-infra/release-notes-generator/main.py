#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import parse_commits, generate_release_notes, get_stats
def cmd_generate(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    commits = parse_commits(text)
    if args.json: print(json.dumps(get_stats(commits), indent=2))
    else: print(generate_release_notes(commits, version=args.version))
def main():
    p = argparse.ArgumentParser(description="Release Notes Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("file", nargs="?", default="-"); g.add_argument("--version", default="Unreleased"); g.add_argument("--json", action="store_true"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
