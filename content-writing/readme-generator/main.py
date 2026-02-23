#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import detect_project, generate_readme, generate_from_template, ProjectInfo
def cmd_generate(args):
    if args.dir: info = detect_project(args.dir); print(generate_readme(info))
    else: print(generate_from_template(args.name or "MyProject", template=args.template or "minimal"))
def main():
    p = argparse.ArgumentParser(description="README Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("--dir"); g.add_argument("--name"); g.add_argument("--template", choices=["minimal","api","cli"]); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
