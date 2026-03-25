#!/usr/bin/env python3
"""API Key Rotator CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import scan, rotate, audit, format_output

def cmd_scan(args):
    inp = getattr(args, "scan_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = scan(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_rotate(args):
    inp = getattr(args, "rotate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = rotate(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_audit(args):
    inp = getattr(args, "audit_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = audit(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="API Key Rotator")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("scan"); p.add_argument("scan_input", nargs="?", default=""); p.set_defaults(func=cmd_scan)
    p = sub.add_parser("rotate"); p.add_argument("rotate_input", nargs="?", default=""); p.set_defaults(func=cmd_rotate)
    p = sub.add_parser("audit"); p.add_argument("audit_input", nargs="?", default=""); p.set_defaults(func=cmd_audit)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
