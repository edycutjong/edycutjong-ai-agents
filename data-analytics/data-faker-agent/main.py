#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.faker import generate_fake_data, export_json, export_csv, list_schemas
def cmd_generate(args):
    data = generate_fake_data(args.schema, count=args.count)
    print(export_csv(data) if args.csv else export_json(data))
def main():
    p = argparse.ArgumentParser(description="Data Faker"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("schema", choices=["user","product","order"]); g.add_argument("--count", type=int, default=10); g.add_argument("--csv", action="store_true"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
