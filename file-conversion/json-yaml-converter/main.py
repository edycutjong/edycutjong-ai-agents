#!/usr/bin/env python3
"""CLI for JSON/YAML/TOML Converter."""
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.converter import convert, validate_json, format_json, detect_format

def cmd_convert(args):
    text = sys.stdin.read() if args.input == "-" else open(args.input).read()
    result = convert(text, args.to, source_format=args.source)
    if args.output: open(args.output, "w").write(result); print(f"✅ Saved to {args.output}")
    else: print(result)

def cmd_validate(args):
    text = sys.stdin.read() if args.input == "-" else open(args.input).read()
    info = validate_json(text)
    if info["valid"]: print(f"✅ Valid JSON ({info['type']}, {info.get('length', '?')} items)")
    else: print(f"❌ Invalid: {info['error']} (line {info['line']}, col {info['col']})")

def cmd_format(args):
    text = sys.stdin.read() if args.input == "-" else open(args.input).read()
    print(format_json(text, indent=args.indent, sort_keys=args.sort, compact=args.compact))

def cmd_detect(args):
    text = sys.stdin.read() if args.input == "-" else open(args.input).read()
    print(f"Detected: {detect_format(text)}")

def main():
    parser = argparse.ArgumentParser(description="JSON/YAML/TOML Converter")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("convert"); p.add_argument("input"); p.add_argument("--to", required=True, choices=["json","yaml","toml"]); p.add_argument("--source", choices=["json","yaml","toml"]); p.add_argument("--output", "-o"); p.set_defaults(func=cmd_convert)
    p = sub.add_parser("validate"); p.add_argument("input"); p.set_defaults(func=cmd_validate)
    p = sub.add_parser("format"); p.add_argument("input"); p.add_argument("--indent", type=int, default=2); p.add_argument("--sort", action="store_true"); p.add_argument("--compact", action="store_true"); p.set_defaults(func=cmd_format)
    p = sub.add_parser("detect"); p.add_argument("input"); p.set_defaults(func=cmd_detect)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
