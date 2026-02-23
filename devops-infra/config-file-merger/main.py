#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.merger import merge_configs, format_result_markdown
def cmd_merge(args):
    configs = [json.loads(open(f).read()) for f in args.files]
    r = merge_configs(configs, strategy=args.strategy)
    if args.report: print(format_result_markdown(r))
    else: print(json.dumps(r.merged, indent=2))
def main():
    p = argparse.ArgumentParser(description="Config File Merger"); s = p.add_subparsers(dest="command", required=True)
    m = s.add_parser("merge"); m.add_argument("files", nargs="+"); m.add_argument("--strategy", default="override"); m.add_argument("--report", action="store_true"); m.set_defaults(func=cmd_merge)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
