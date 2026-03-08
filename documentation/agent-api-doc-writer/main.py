"""
Documentation Agent (documentation/ category stub) — generates API docs and architecture overviews.
Usage: python main.py <source_file> [--output docs/]
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Documentation Agent] Paste source code or describe your project to auto-generate README, API reference, and architecture documentation."


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
    doc = f"# {name}\n\n## API Reference\n\n"
    for fn, params in fns:
        doc += f"### `{fn}({params})`\n\n_No description yet. Add a docstring._\n\n"
    if args.output:
        open(args.output, "w").write(doc)
        print(f"✅ Documentation written to {args.output}")
    else:
        print(doc)

if __name__ == "__main__":
    main()
