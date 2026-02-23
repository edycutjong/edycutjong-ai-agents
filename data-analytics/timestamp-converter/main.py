#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.converter import unix_to_datetime, iso_to_unix, now_utc, format_result_markdown
def cmd_unix(args): print(format_result_markdown(unix_to_datetime(args.timestamp)))
def cmd_iso(args): print(format_result_markdown(iso_to_unix(args.iso)))
def cmd_now(args): print(format_result_markdown(now_utc()))
def main():
    p = argparse.ArgumentParser(description="Timestamp Converter"); s = p.add_subparsers(dest="command", required=True)
    u = s.add_parser("unix"); u.add_argument("timestamp", type=float); u.set_defaults(func=cmd_unix)
    i = s.add_parser("iso"); i.add_argument("iso"); i.set_defaults(func=cmd_iso)
    n = s.add_parser("now"); n.set_defaults(func=cmd_now)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
