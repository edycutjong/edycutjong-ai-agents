#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_palette, format_result_markdown
def cmd_generate(args): print(format_result_markdown(generate_palette(args.color, scheme=args.scheme)))
def main():
    p = argparse.ArgumentParser(description="Color Palette Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("color"); g.add_argument("--scheme", default="complementary"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
