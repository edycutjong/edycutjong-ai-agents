#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.encoder import encode, decode, is_valid_base64, encode_url_safe, decode_url_safe, format_result_markdown
def cmd_encode(args):
    if args.url_safe: print(encode_url_safe(args.text))
    else: print(format_result_markdown(encode(args.text)))
def cmd_decode(args):
    if args.url_safe: print(decode_url_safe(args.text))
    else: print(format_result_markdown(decode(args.text)))
def cmd_auto(args):
    if is_valid_base64(args.text): print(format_result_markdown(decode(args.text)))
    else: print(format_result_markdown(encode(args.text)))
def main():
    p = argparse.ArgumentParser(description="Base64 Encoder/Decoder"); s = p.add_subparsers(dest="command", required=True)
    e = s.add_parser("encode"); e.add_argument("text"); e.add_argument("--url-safe", action="store_true"); e.set_defaults(func=cmd_encode)
    d = s.add_parser("decode"); d.add_argument("text"); d.add_argument("--url-safe", action="store_true"); d.set_defaults(func=cmd_decode)
    a = s.add_parser("auto"); a.add_argument("text"); a.set_defaults(func=cmd_auto)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
