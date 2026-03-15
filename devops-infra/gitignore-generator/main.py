#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate, format_result_markdown, get_languages
def cmd_generate(args): print(format_result_markdown(generate(args.templates)))
def cmd_list(args):
    for t in get_languages(): print(t)
def main():
    p = argparse.ArgumentParser(description="Gitignore Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("templates", nargs="+"); g.set_defaults(func=cmd_generate)
    l = s.add_parser("list"); l.set_defaults(func=cmd_list)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
