#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.encoder import encode, decode, detect_and_convert, format_result_markdown
def cmd_encode(args): print(format_result_markdown(encode(args.text, url_safe=args.url_safe)))
def cmd_decode(args): print(format_result_markdown(decode(args.text, url_safe=args.url_safe)))
def cmd_auto(args): print(format_result_markdown(detect_and_convert(args.text)))
def main():
    p = argparse.ArgumentParser(description="Base64 Encoder/Decoder"); s = p.add_subparsers(dest="command", required=True)
    e = s.add_parser("encode"); e.add_argument("text"); e.add_argument("--url-safe", action="store_true"); e.set_defaults(func=cmd_encode)
    d = s.add_parser("decode"); d.add_argument("text"); d.add_argument("--url-safe", action="store_true"); d.set_defaults(func=cmd_decode)
    a = s.add_parser("auto"); a.add_argument("text"); a.set_defaults(func=cmd_auto)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
