#!/usr/bin/env python3
"""Token Price Tracker CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import track, alert, portfolio, format_output

def cmd_track(args):
    inp = getattr(args, "track_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = track(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_alert(args):
    inp = getattr(args, "alert_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = alert(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_portfolio(args):
    inp = getattr(args, "portfolio_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = portfolio(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Token Price Tracker")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("track"); p.add_argument("track_input", nargs="?", default=""); p.set_defaults(func=cmd_track)
    p = sub.add_parser("alert"); p.add_argument("alert_input", nargs="?", default=""); p.set_defaults(func=cmd_alert)
    p = sub.add_parser("portfolio"); p.add_argument("portfolio_input", nargs="?", default=""); p.set_defaults(func=cmd_portfolio)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
