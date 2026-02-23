#!/usr/bin/env python3
"""CLI for Contract Analyzer."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import analyze_contract, format_analysis_markdown

def cmd_analyze(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    result = analyze_contract(text)
    if args.json: print(json.dumps(result.to_dict(), indent=2))
    else: print(format_analysis_markdown(result))

def main():
    parser = argparse.ArgumentParser(description="Contract Analyzer")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze"); p.add_argument("file"); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_analyze)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
