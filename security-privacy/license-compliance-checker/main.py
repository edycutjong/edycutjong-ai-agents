#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.checker import check_compatibility, parse_requirements_txt, parse_package_json, format_report_markdown, LicenseInfo
def cmd_check(args):
    text = open(args.file).read()
    if args.file.endswith(".json"): deps = parse_package_json(text)
    else: deps = parse_requirements_txt(text)
    issues = check_compatibility(args.license, deps)
    print(format_report_markdown(args.license, deps, issues))
def main():
    p = argparse.ArgumentParser(description="License Compliance Checker"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("check"); c.add_argument("file"); c.add_argument("--license", default="MIT"); c.set_defaults(func=cmd_check)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
