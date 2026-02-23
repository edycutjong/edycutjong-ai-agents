#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.converter import convert_json_string_to_yaml, convert_yaml_string_to_json, detect_format
def cmd_convert(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    fmt = detect_format(text)
    if fmt == "json": print(convert_json_string_to_yaml(text))
    else: print(convert_yaml_string_to_json(text))
def main():
    p = argparse.ArgumentParser(description="YAML-JSON Converter"); s = p.add_subparsers(dest="command", required=True)
    c = s.add_parser("convert"); c.add_argument("file", nargs="?", default="-"); c.set_defaults(func=cmd_convert)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
