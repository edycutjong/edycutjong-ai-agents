#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.lookup import lookup_ip, format_result_markdown
def cmd_lookup(args): print(format_result_markdown(lookup_ip(args.ip)))
def main():
    p = argparse.ArgumentParser(description="IP Geolocation Lookup"); s = p.add_subparsers(dest="command", required=True)
    l = s.add_parser("lookup"); l.add_argument("ip"); l.set_defaults(func=cmd_lookup)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
