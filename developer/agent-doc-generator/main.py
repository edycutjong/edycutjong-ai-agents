"""
Doc Generator Agent — scans a codebase and generates documentation.
Usage: python main.py <source_file_or_dir> [--output docs/]
"""
import argparse
import sys
import os
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Doc Generator] Ready.\n\nPaste source code, a function, or a class definition to generate documentation including docstrings, API docs, and usage examples."


def extract_docstrings(code: str) -> list:
    pattern = re.compile(
        r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*[\w\[\], ]+)?\s*:\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')?',
        re.DOTALL
    )
    results = []
    for m in pattern.finditer(code):
        name = m.group(1)
        params = m.group(2).strip()
        docstring = (m.group(3) or m.group(4) or "").strip()
        results.append({"name": name, "params": params, "doc": docstring})
    return results


def generate_markdown_docs(source_path: str, functions: list) -> str:
    lines = [f"# API Documentation\n\n**Source:** `{source_path}`\n"]
    for fn in functions:
        lines.append(f"## `{fn['name']}({fn['params']})`\n")
        if fn["doc"]:
            lines.append(f"{fn['doc']}\n")
        else:
            lines.append("_No docstring provided._\n")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate documentation from source code")
    parser.add_argument("source", nargs="?", help="Source file to document")
    parser.add_argument("--output", default="", help="Output markdown file path")
    args = parser.parse_args()

    if not args.source:
        print("Doc Generator Agent")
        print("Usage: python main.py <source.py> [--output docs/api.md]")
        sys.exit(0)

    if not os.path.isfile(args.source):
        print(f"File not found: {args.source}")
        sys.exit(1)

    with open(args.source) as f:
        code = f.read()

    functions = extract_docstrings(code)
    if not functions:
        print("No functions found to document.")
        sys.exit(0)

    docs = generate_markdown_docs(args.source, functions)
    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            f.write(docs)
        print(f"✅ Docs written to {args.output}")
    else:
        print(docs)


if __name__ == "__main__":
    main()
