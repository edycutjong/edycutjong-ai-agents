#!/usr/bin/env python3
"""CLI for Config File Generator."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import (
    generate_config, generate_multiple, list_config_types,
    list_presets, detect_project_type,
)

def cmd_generate(args):
    result = generate_config(args.type, preset=args.preset, overrides=json.loads(args.override) if args.override else None)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr); sys.exit(1)
    if args.save:
        os.makedirs(os.path.dirname(result["filename"]) or ".", exist_ok=True)
        with open(result["filename"], "w") as f: f.write(result["content"])
        print(f"✅ Saved {result['filename']}")
    else:
        print(f"# {result['filename']}\n{result['content']}")

def cmd_list(args):
    for ct in list_config_types():
        print(f"  {ct['type']:<20} {ct['description']:<30} → {ct['filename']}")
        print(f"    Presets: {', '.join(ct['presets'])}")

def cmd_presets(args):
    presets = list_presets(args.type)
    if not presets: print(f"Unknown type: {args.type}"); return
    print(f"Presets for {args.type}: {', '.join(presets)}")

def cmd_scaffold(args):
    types = args.types.split(",")
    results = generate_multiple(types, preset=args.preset)
    for r in results:
        if "error" in r: print(f"Error: {r['error']}"); continue
        if args.save:
            os.makedirs(os.path.dirname(r["filename"]) or ".", exist_ok=True)
            with open(r["filename"], "w") as f: f.write(r["content"])
            print(f"✅ {r['filename']}")
        else:
            print(f"# {r['filename']}\n{r['content']}\n---")

def cmd_detect(args):
    files = os.listdir(args.path or ".")
    project_type = detect_project_type(files)
    print(f"Detected: {project_type}")

def main():
    parser = argparse.ArgumentParser(description="Config File Generator")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate"); p.add_argument("type"); p.add_argument("--preset", default="default"); p.add_argument("--save", action="store_true"); p.add_argument("--override", help="JSON overrides"); p.set_defaults(func=cmd_generate)
    p = sub.add_parser("list"); p.set_defaults(func=cmd_list)
    p = sub.add_parser("presets"); p.add_argument("type"); p.set_defaults(func=cmd_presets)
    p = sub.add_parser("scaffold"); p.add_argument("types", help="Comma-separated config types"); p.add_argument("--preset", default="default"); p.add_argument("--save", action="store_true"); p.set_defaults(func=cmd_scaffold)
    p = sub.add_parser("detect"); p.add_argument("--path", default="."); p.set_defaults(func=cmd_detect)
    args = parser.parse_args(); args.func(args)

if __name__ == "__main__": main()
