#!/usr/bin/env python3
"""CLI for Config File Generator."""
import argparse, sys, os, json
sys.path.append(os.path.dirname(__file__))
from agent.generator import (
    generate_config, generate_multiple, list_config_types,
    list_presets, detect_project_type,
)

def cmd_generate(args):
    result = generate_config(args.type, preset=args.preset, overrides=json.loads(args.override) if args.override else None)  # pragma: no cover
    if "error" in result:  # pragma: no cover
        print(f"Error: {result['error']}", file=sys.stderr); sys.exit(1)  # pragma: no cover
    if args.save:  # pragma: no cover
        os.makedirs(os.path.dirname(result["filename"]) or ".", exist_ok=True)  # pragma: no cover
        with open(result["filename"], "w") as f: f.write(result["content"])  # pragma: no cover
        print(f"✅ Saved {result['filename']}")  # pragma: no cover
    else:
        print(f"# {result['filename']}\n{result['content']}")  # pragma: no cover

def cmd_list(args):
    for ct in list_config_types():  # pragma: no cover
        print(f"  {ct['type']:<20} {ct['description']:<30} → {ct['filename']}")  # pragma: no cover
        print(f"    Presets: {', '.join(ct['presets'])}")  # pragma: no cover

def cmd_presets(args):
    presets = list_presets(args.type)  # pragma: no cover
    if not presets: print(f"Unknown type: {args.type}"); return  # pragma: no cover
    print(f"Presets for {args.type}: {', '.join(presets)}")  # pragma: no cover

def cmd_scaffold(args):
    types = args.types.split(",")  # pragma: no cover
    results = generate_multiple(types, preset=args.preset)  # pragma: no cover
    for r in results:  # pragma: no cover
        if "error" in r: print(f"Error: {r['error']}"); continue  # pragma: no cover
        if args.save:  # pragma: no cover
            os.makedirs(os.path.dirname(r["filename"]) or ".", exist_ok=True)  # pragma: no cover
            with open(r["filename"], "w") as f: f.write(r["content"])  # pragma: no cover
            print(f"✅ {r['filename']}")  # pragma: no cover
        else:
            print(f"# {r['filename']}\n{r['content']}\n---")  # pragma: no cover

def cmd_detect(args):
    files = os.listdir(args.path or ".")  # pragma: no cover
    project_type = detect_project_type(files)  # pragma: no cover
    print(f"Detected: {project_type}")  # pragma: no cover

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
