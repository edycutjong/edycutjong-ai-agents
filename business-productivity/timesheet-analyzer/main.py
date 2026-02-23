#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import parse_csv_timesheet, analyze_timesheet, format_report_markdown
def cmd_analyze(args):
    csv = sys.stdin.read() if args.file == "-" else open(args.file).read()
    entries = parse_csv_timesheet(csv)
    report = analyze_timesheet(entries, daily_target=args.target)
    if args.json: print(json.dumps(report.to_dict(), indent=2))
    else: print(format_report_markdown(report))
def main():
    p = argparse.ArgumentParser(description="Timesheet Analyzer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("file"); a.add_argument("--target", type=float, default=8.0); a.add_argument("--json", action="store_true"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
