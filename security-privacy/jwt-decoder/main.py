#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.decoder import decode_jwt, format_result_markdown
def cmd_decode(args): print(format_result_markdown(decode_jwt(args.token)))
def main():
    p = argparse.ArgumentParser(description="JWT Decoder"); s = p.add_subparsers(dest="command", required=True)
    d = s.add_parser("decode"); d.add_argument("token"); d.set_defaults(func=cmd_decode)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
