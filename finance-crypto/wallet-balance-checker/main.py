#!/usr/bin/env python3
"""Wallet Balance Checker CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import check, portfolio, history, format_output

def cmd_check(args):
    inp = getattr(args, "check_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = check(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_portfolio(args):
    inp = getattr(args, "portfolio_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = portfolio(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_history(args):
    inp = getattr(args, "history_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = history(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Wallet Balance Checker")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check"); p.add_argument("check_input", nargs="?", default=""); p.set_defaults(func=cmd_check)
    p = sub.add_parser("portfolio"); p.add_argument("portfolio_input", nargs="?", default=""); p.set_defaults(func=cmd_portfolio)
    p = sub.add_parser("history"); p.add_argument("history_input", nargs="?", default=""); p.set_defaults(func=cmd_history)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
