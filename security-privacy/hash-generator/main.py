#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_hash, multi_hash, format_result_markdown
def cmd_hash(args): print(format_result_markdown(generate_hash(args.text, algorithm=args.algo)))
def cmd_multi(args):
    for algo, h in multi_hash(args.text).items(): print(f"{algo}: {h}")
def main():
    p = argparse.ArgumentParser(description="Hash Generator"); s = p.add_subparsers(dest="command", required=True)
    h = s.add_parser("hash"); h.add_argument("text"); h.add_argument("--algo", default="sha256"); h.set_defaults(func=cmd_hash)
    m = s.add_parser("multi"); m.add_argument("text"); m.set_defaults(func=cmd_multi)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
