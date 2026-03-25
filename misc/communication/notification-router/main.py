#!/usr/bin/env python3
"""Notification Router CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import route, configure, status, format_output

def cmd_route(args):
    inp = getattr(args, "route_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = route(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_configure(args):
    inp = getattr(args, "configure_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = configure(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_status(args):
    inp = getattr(args, "status_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = status(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Notification Router")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("route"); p.add_argument("route_input", nargs="?", default=""); p.set_defaults(func=cmd_route)
    p = sub.add_parser("configure"); p.add_argument("configure_input", nargs="?", default=""); p.set_defaults(func=cmd_configure)
    p = sub.add_parser("status"); p.add_argument("status_input", nargs="?", default=""); p.set_defaults(func=cmd_status)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
