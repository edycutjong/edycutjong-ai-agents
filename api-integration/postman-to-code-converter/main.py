#!/usr/bin/env python3
"""CLI for Postman to Code Converter."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.converter import parse_collection, convert_request, convert_collection, GENERATORS

def cmd_convert(args):
    collection = json.load(open(args.collection))
    print(convert_collection(collection, args.language))

def cmd_languages(args):
    for lang in GENERATORS: print(f"  {lang}")

def main():
    parser = argparse.ArgumentParser(description="Postman to Code Converter")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("convert"); p.add_argument("collection"); p.add_argument("--language", "-l", default="python", choices=list(GENERATORS.keys())); p.set_defaults(func=cmd_convert)
    p = sub.add_parser("languages"); p.set_defaults(func=cmd_languages)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
