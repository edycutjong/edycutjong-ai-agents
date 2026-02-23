#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.analyzer import analyze_password, format_result_markdown
def cmd_analyze(args):
    pw = args.password if args.password else input("Password: ")
    r = analyze_password(pw)
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Password Strength Analyzer"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("analyze"); a.add_argument("password", nargs="?"); a.set_defaults(func=cmd_analyze)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
