#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.scanner import analyze_ports, format_result_markdown
def cmd_scan(args): print(format_result_markdown(analyze_ports([int(p) for p in args.ports.split(",")], target=args.target)))
def main():
    p = argparse.ArgumentParser(description="Port Scanner"); s = p.add_subparsers(dest="command", required=True)
    sc = s.add_parser("scan"); sc.add_argument("ports"); sc.add_argument("--target", default="localhost"); sc.set_defaults(func=cmd_scan)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
