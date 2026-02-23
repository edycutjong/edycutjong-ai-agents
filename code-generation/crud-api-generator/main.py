#!/usr/bin/env python3
import argparse, sys, os
sys.path.append(os.path.dirname(__file__))
from agent.generator import Model, ModelField, generate_express_routes, generate_fastapi_routes, parse_model_definition, list_endpoints
def cmd_generate(args):
    model = parse_model_definition(args.model)
    if args.framework == "express": print(generate_express_routes(model))
    else: print(generate_fastapi_routes(model))
def main():
    p = argparse.ArgumentParser(description="CRUD API Generator"); s = p.add_subparsers(dest="command", required=True)
    g = s.add_parser("generate"); g.add_argument("model", help="Model definition e.g. 'User: name:string, email:string'"); g.add_argument("--framework", choices=["express","fastapi"], default="express"); g.set_defaults(func=cmd_generate)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
