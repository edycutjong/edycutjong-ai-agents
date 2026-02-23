#!/usr/bin/env python3
"""CLI for Training Data Generator."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_from_template, generate_variations, validate_dataset, export_dataset, format_stats_markdown, TrainingExample, TEMPLATES

def cmd_generate(args):
    variables = dict(v.split("=") for v in args.vars) if args.vars else {}
    examples = generate_from_template(args.category, variables, count=args.count)
    print(export_dataset(examples, fmt=args.format))

def cmd_validate(args):
    data = json.load(open(args.file))
    examples = [TrainingExample(**d) for d in data]
    stats = validate_dataset(examples)
    print(format_stats_markdown(stats))

def cmd_templates(args):
    for cat, tmpls in TEMPLATES.items():
        print(f"  {cat}: {len(tmpls)} templates")

def main():
    parser = argparse.ArgumentParser(description="Training Data Generator")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate"); p.add_argument("--category", required=True); p.add_argument("--count", type=int, default=5); p.add_argument("--vars", nargs="*"); p.add_argument("--format", default="alpaca", choices=["alpaca","chat","completion","jsonl"]); p.set_defaults(func=cmd_generate)
    p = sub.add_parser("validate"); p.add_argument("file"); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("templates"); p.set_defaults(func=cmd_templates)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
