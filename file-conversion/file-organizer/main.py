#!/usr/bin/env python3
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.organizer import organize_file_list, format_result_markdown
def cmd_organize(args):
    text = sys.stdin.read() if args.file == "-" else open(args.file).read()
    r = organize_file_list(json.loads(text))
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="File Organizer"); s = p.add_subparsers(dest="command", required=True)
    o = s.add_parser("organize"); o.add_argument("file", nargs="?", default="-"); o.set_defaults(func=cmd_organize)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
