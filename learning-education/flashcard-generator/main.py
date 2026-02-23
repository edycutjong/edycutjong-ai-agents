#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_from_topic, generate_from_terms, format_deck_markdown, export_anki
def cmd_generate(args):
    deck = generate_from_topic(args.topic, count=args.count)
    if args.anki: print(export_anki(deck))
    elif args.json: print(json.dumps(deck.to_dict(), indent=2))
    else: print(format_deck_markdown(deck))
def main():
    p = argparse.ArgumentParser(description="Flashcard Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("topic"); g.add_argument("--count", type=int, default=10); g.add_argument("--anki", action="store_true"); g.add_argument("--json", action="store_true"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
