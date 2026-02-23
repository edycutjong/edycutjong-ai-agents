#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.detector import analyze_email, format_result_markdown
def cmd_analyze(args):
    body = sys.stdin.read() if args.body == "-" else args.body
    r = analyze_email(args.subject, body, sender=args.sender or "")
    if args.json: print(json.dumps(r.to_dict(), indent=2))
    else: print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Phishing Email Detector"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("--subject", default=""); a.add_argument("--body", default="-"); a.add_argument("--sender", default=""); a.add_argument("--json", action="store_true"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
