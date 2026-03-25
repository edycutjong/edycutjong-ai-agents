#!/usr/bin/env python3
"""Discord Bot Builder CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import generate, scaffold, deploy, format_output

def cmd_generate(args):
    inp = getattr(args, "generate_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = generate(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_scaffold(args):
    inp = getattr(args, "scaffold_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = scaffold(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_deploy(args):
    inp = getattr(args, "deploy_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = deploy(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Discord Bot Builder")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate"); p.add_argument("generate_input", nargs="?", default=""); p.set_defaults(func=cmd_generate)
    p = sub.add_parser("scaffold"); p.add_argument("scaffold_input", nargs="?", default=""); p.set_defaults(func=cmd_scaffold)
    p = sub.add_parser("deploy"); p.add_argument("deploy_input", nargs="?", default=""); p.set_defaults(func=cmd_deploy)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
