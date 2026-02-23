#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.writer import WorkflowConfig, generate_workflow, workflow_to_yaml, list_templates, format_templates_markdown
def cmd_generate(args):
    config = WorkflowConfig(template=args.template, name=args.name or "")
    workflow = generate_workflow(config)
    print(workflow_to_yaml(workflow))
def cmd_list(args):
    print(format_templates_markdown())
def main():
    p = argparse.ArgumentParser(description="GitHub Actions Writer"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("template"); g.add_argument("--name"); g.set_defaults(func=cmd_generate)
    l = s.add_parser("list"); l.set_defaults(func=cmd_list)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
