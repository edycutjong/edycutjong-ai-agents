#!/usr/bin/env python3
"""Meal Prep Planner CLI."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.core import plan, grocery, nutrition, format_output

def cmd_plan(args):
    inp = getattr(args, "plan_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = plan(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_grocery(args):
    inp = getattr(args, "grocery_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = grocery(inp)
    print(format_output(result, "json" if args.json else "text"))

def cmd_nutrition(args):
    inp = getattr(args, "nutrition_input", "") or ""
    if inp == "-": inp = sys.stdin.read().strip()
    result = nutrition(inp)
    print(format_output(result, "json" if args.json else "text"))

def main():
    parser = argparse.ArgumentParser(description="Meal Prep Planner")
    parser.add_argument("--json", action="store_true", help="JSON output")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("plan"); p.add_argument("plan_input", nargs="?", default=""); p.set_defaults(func=cmd_plan)
    p = sub.add_parser("grocery"); p.add_argument("grocery_input", nargs="?", default=""); p.set_defaults(func=cmd_grocery)
    p = sub.add_parser("nutrition"); p.add_argument("nutrition_input", nargs="?", default=""); p.set_defaults(func=cmd_nutrition)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
