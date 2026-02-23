#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.optimizer import analyze_dockerfile, format_analysis_markdown
def cmd_analyze(args):
    content = sys.stdin.read() if args.file == "-" else open(args.file).read()
    result = analyze_dockerfile(content)
    if args.json: print(json.dumps(result.to_dict(), indent=2))
    else: print(format_analysis_markdown(result))
def main():
    p = argparse.ArgumentParser(description="Dockerfile Optimizer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("file"); a.add_argument("--json", action="store_true"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
