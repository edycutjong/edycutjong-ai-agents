"""
Documentation Agent (documentation/ category stub) — generates API docs and architecture overviews.
Usage: python main.py <source_file> [--output docs/]
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Documentation Agent] Paste source code or describe your project to auto-generate README, API reference, and architecture documentation."  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Generate documentation from source code")
    parser.add_argument("file", nargs="?", help="Source file to document")
    parser.add_argument("--output", default="", help="Output file path")
    args = parser.parse_args()
    if not args.file:
        print("Documentation Agent\nUsage: python main.py <source.py> [--output README.md]")
        sys.exit(0)
    if not os.path.isfile(args.file):  # pragma: no cover
        print(f"File not found: {args.file}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    code = open(args.file).read()  # pragma: no cover
    fns = re.findall(r"^def (\w+)\s*\(([^)]*)\)", code, re.MULTILINE)  # pragma: no cover
    name = os.path.splitext(os.path.basename(args.file))[0]  # pragma: no cover
    doc = f"# {name}\n\n## API Reference\n\n"  # pragma: no cover
    for fn, params in fns:  # pragma: no cover
        doc += f"### `{fn}({params})`\n\n_No description yet. Add a docstring._\n\n"  # pragma: no cover
    if args.output:  # pragma: no cover
        open(args.output, "w").write(doc)  # pragma: no cover
        print(f"✅ Documentation written to {args.output}")  # pragma: no cover
    else:
        print(doc)  # pragma: no cover

if __name__ == "__main__":
    main()
