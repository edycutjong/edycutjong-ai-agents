#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_quiz, format_quiz_markdown
def cmd_generate(args):
    quiz = generate_quiz(args.topic, count=args.count)
    if args.json: print(json.dumps(quiz.to_dict(), indent=2))
    else: print(format_quiz_markdown(quiz))
def main():
    p = argparse.ArgumentParser(description="Quiz Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("topic"); g.add_argument("--count", type=int, default=5); g.add_argument("--json", action="store_true"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
