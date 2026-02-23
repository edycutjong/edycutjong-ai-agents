#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import generate_project, write_project, list_templates, format_project_markdown
def cmd_generate(args):
    project = generate_project(args.name, args.template)
    if args.output: written = write_project(project, args.output); print(f"Created {len(written)} files in {args.output}")
    else: print(format_project_markdown(project))
def cmd_list(args):
    for k, v in list_templates().items(): print(f"  {k}: {v}")
def main():
    p = argparse.ArgumentParser(description="Boilerplate Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("name"); g.add_argument("--template", required=True); g.add_argument("--output"); g.set_defaults(func=cmd_generate)
    l = s.add_parser("list"); l.set_defaults(func=cmd_list)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
