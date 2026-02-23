#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.checker import check_password, format_result_markdown
def cmd_check(args): print(format_result_markdown(check_password(args.password)))
def main():
    p = argparse.ArgumentParser(description="Password Strength Checker"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("check"); c.add_argument("password"); c.set_defaults(func=cmd_check)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
