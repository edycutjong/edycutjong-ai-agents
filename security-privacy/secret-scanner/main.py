#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.scanner import scan_text, scan_file, scan_directory, format_report_markdown
def cmd_scan(args):
    if os.path.isdir(args.path): matches = scan_directory(args.path)
    elif os.path.isfile(args.path): matches = scan_file(args.path)
    else: matches = scan_text(sys.stdin.read())
    if args.json: print(json.dumps([m.to_dict() for m in matches], indent=2))
    else: print(format_report_markdown(matches))
def main():
    p = argparse.ArgumentParser(description="Secret Scanner"); s = p.add_subparsers(dest="command", required=True)
    sc = s.add_parser("scan"); sc.add_argument("path", nargs="?", default="."); sc.add_argument("--json", action="store_true"); sc.set_defaults(func=cmd_scan)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
