#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.auditor import audit_html, format_result_markdown
def cmd_audit(args):
    html = sys.stdin.read() if args.file == "-" else open(args.file).read()
    r = audit_html(html)
    print(format_result_markdown(r))
def main():
    p = argparse.ArgumentParser(description="Accessibility Auditor"); s = p.add_subparsers(dest="command", required=True)
    a = s.add_parser("audit"); a.add_argument("file", nargs="?", default="-"); a.set_defaults(func=cmd_audit)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
