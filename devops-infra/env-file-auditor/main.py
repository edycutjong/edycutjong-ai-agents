#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.auditor import audit_env, compare_envs, format_audit_markdown, generate_env_template
def cmd_audit(args):
    text = open(args.file).read()
    result = audit_env(text)
    if args.json: print(json.dumps(result.to_dict(), indent=2))
    else: print(format_audit_markdown(result))
def cmd_compare(args):
    r = compare_envs(open(args.file_a).read(), open(args.file_b).read())
    print(json.dumps(r.to_dict(), indent=2))
def cmd_template(args):
    print(generate_env_template(open(args.file).read()))
def main():
    p = argparse.ArgumentParser(description="Env File Auditor"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("audit"); a.add_argument("file"); a.add_argument("--json", action="store_true"); a.set_defaults(func=cmd_audit)
    c = s.add_parser("compare"); c.add_argument("file_a"); c.add_argument("file_b"); c.set_defaults(func=cmd_compare)
    t = s.add_parser("template"); t.add_argument("file"); t.set_defaults(func=cmd_template)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
