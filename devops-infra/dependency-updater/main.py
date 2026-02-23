#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.updater import parse_requirements, analyze_dependencies, format_result_markdown
def cmd_analyze(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    deps = parse_requirements(text, filename=args.file)
    r = analyze_dependencies(deps)
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Dependency Updater"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("file", nargs="?", default="-"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
