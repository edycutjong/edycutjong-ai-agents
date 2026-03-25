#!/usr/bin/env python3
"""Dataset Bias Auditor CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import audit, score, remediate, format_output

def cmd_audit(args):
    inp = getattr(args, "audit_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = audit(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_score(args):
    inp = getattr(args, "score_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = score(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_remediate(args):
    inp = getattr(args, "remediate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = remediate(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Dataset Bias Auditor")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("audit"); p.add_argument("audit_input", nargs="?", default=""); p.set_defaults(func=cmd_audit)
    p = sub.add_parser("score"); p.add_argument("score_input", nargs="?", default=""); p.set_defaults(func=cmd_score)
    p = sub.add_parser("remediate"); p.add_argument("remediate_input", nargs="?", default=""); p.set_defaults(func=cmd_remediate)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
