#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_compose, list_templates
def cmd_generate(args):
    print(generate_compose(args.services))
def cmd_list(args):
    for t in list_templates(): print(f"  - {t}")
def main():
    p = argparse.ArgumentParser(description="Docker Compose Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("services", nargs="+"); g.set_defaults(func=cmd_generate)
    l = s.add_parser("list"); l.set_defaults(func=cmd_list)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
