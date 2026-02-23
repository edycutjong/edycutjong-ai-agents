#!/usr/bin/env python3
"""CLI for Prompt Optimizer."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.optimizer import analyze_prompt, optimize_prompt, compare_prompts, format_analysis_markdown

def cmd_analyze(args):
    prompt = sys.stdin.read() if args.prompt == "-" else args.prompt
    result = analyze_prompt(prompt)
    if args.json: print(json.dumps(result.to_dict(), indent=2))
    else: print(format_analysis_markdown(result))

def cmd_optimize(args):
    prompt = sys.stdin.read() if args.prompt == "-" else args.prompt
    print(optimize_prompt(prompt))

def cmd_compare(args):
    r = compare_prompts(args.prompt_a, args.prompt_b)
    print(f"Prompt A: {r['prompt_a_score']}/100\nPrompt B: {r['prompt_b_score']}/100\nWinner: {r['winner']} (+{r['difference']})")

def main():
    parser = argparse.ArgumentParser(description="Prompt Optimizer")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze"); p.add_argument("prompt"); p.add_argument("--json", action="store_true"); p.set_defaults(func=cmd_analyze)
    p = sub.add_parser("optimize"); p.add_argument("prompt"); p.set_defaults(func=cmd_optimize)
    p = sub.add_parser("compare"); p.add_argument("prompt_a"); p.add_argument("prompt_b"); p.set_defaults(func=cmd_compare)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
