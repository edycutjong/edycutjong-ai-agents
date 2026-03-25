#!/usr/bin/env python3
"""Meditation Guide CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import generate, breathe, affirm, format_output

def cmd_generate(args):
    inp = getattr(args, "generate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = generate(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_breathe(args):
    inp = getattr(args, "breathe_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = breathe(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_affirm(args):
    inp = getattr(args, "affirm_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = affirm(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Meditation Guide")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate"); p.add_argument("generate_input", nargs="?", default=""); p.set_defaults(func=cmd_generate)
    p = sub.add_parser("breathe"); p.add_argument("breathe_input", nargs="?", default=""); p.set_defaults(func=cmd_breathe)
    p = sub.add_parser("affirm"); p.add_argument("affirm_input", nargs="?", default=""); p.set_defaults(func=cmd_affirm)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
