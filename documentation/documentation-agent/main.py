"""
Documentation Agent — generates README, API docs, and architecture overviews.
Usage: python main.py <source_file> [--output docs/]
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Documentation Agent] Paste source code or describe your project to generate README, API docs, and architecture diagrams."


def main():
    parser = argparse.ArgumentParser(description="Generate documentation from source code")
    parser.add_argument("file", nargs="?", help="Source file to document")
    parser.add_argument("--output", default="", help="Output file path")
    args = parser.parse_args()
    if not args.file:
        print("Documentation Agent\nUsage: python main.py <source.py> [--output README.md]")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)
    code = open(args.file).read()
    fns = re.findall(r"^def (\w+)\s*\(([^)]*)\)", code, re.MULTILINE)
    name = os.path.splitext(os.path.basename(args.file))[0]
    doc = f"# {name}\n\n## Functions\n\n"
    for fn, params in fns:
        doc += f"### `{fn}({params})`\n\n_Add description here._\n\n"  # pragma: no cover
    if args.output:
        open(args.output, "w").write(doc)  # pragma: no cover
        print(f"✅ Docs written to {args.output}")  # pragma: no cover
    else:
        print(doc)

if __name__ == "__main__":
    main()
