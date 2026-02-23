#!/usr/bin/env python3
"""CLI for Competitive Analysis Agent."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import Competitor, run_analysis, format_report_markdown

def cmd_analyze(args):
    data = json.load(open(args.config))
    your = Competitor(**data["your_product"])
    comps = [Competitor(**c) for c in data.get("competitors", [])]
    report = run_analysis(your, comps)
    if args.json: print(json.dumps(report.to_dict(), indent=2))
    else: print(format_report_markdown(report))

def main():
    parser = argparse.ArgumentParser(description="Competitive Analysis Agent")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze"); p.add_argument("config"); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_analyze)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
