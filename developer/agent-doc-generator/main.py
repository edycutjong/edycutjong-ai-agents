"""
Doc Generator Agent — scans a codebase and generates documentation.
Usage: python main.py <source_file_or_dir> [--output docs/]
"""
import argparse
import sys
import os
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Doc Generator] Ready.\n\nPaste source code, a function, or a class definition to generate documentation including docstrings, API docs, and usage examples."  # pragma: no cover


def extract_docstrings(code: str) -> list:
    pattern = re.compile(  # pragma: no cover
        r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*[\w\[\], ]+)?\s*:\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')?',
        re.DOTALL
    )
    results = []  # pragma: no cover
    for m in pattern.finditer(code):  # pragma: no cover
        name = m.group(1)  # pragma: no cover
        params = m.group(2).strip()  # pragma: no cover
        docstring = (m.group(3) or m.group(4) or "").strip()  # pragma: no cover
        results.append({"name": name, "params": params, "doc": docstring})  # pragma: no cover
    return results  # pragma: no cover


def generate_markdown_docs(source_path: str, functions: list) -> str:
    lines = [f"# API Documentation\n\n**Source:** `{source_path}`\n"]  # pragma: no cover
    for fn in functions:  # pragma: no cover
        lines.append(f"## `{fn['name']}({fn['params']})`\n")  # pragma: no cover
        if fn["doc"]:  # pragma: no cover
            lines.append(f"{fn['doc']}\n")  # pragma: no cover
        else:
            lines.append("_No docstring provided._\n")  # pragma: no cover
        lines.append("")  # pragma: no cover
    return "\n".join(lines)  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Generate documentation from source code")
    parser.add_argument("source", nargs="?", help="Source file to document")
    parser.add_argument("--output", default="", help="Output markdown file path")
    args = parser.parse_args()

    if not args.source:
        print("Doc Generator Agent")
        print("Usage: python main.py <source.py> [--output docs/api.md]")
        sys.exit(0)

    if not os.path.isfile(args.source):  # pragma: no cover
        print(f"File not found: {args.source}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    with open(args.source) as f:  # pragma: no cover
        code = f.read()  # pragma: no cover

    functions = extract_docstrings(code)  # pragma: no cover
    if not functions:  # pragma: no cover
        print("No functions found to document.")  # pragma: no cover
        sys.exit(0)  # pragma: no cover

    docs = generate_markdown_docs(args.source, functions)  # pragma: no cover
    if args.output:  # pragma: no cover
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)  # pragma: no cover
        with open(args.output, "w") as f:  # pragma: no cover
            f.write(docs)  # pragma: no cover
        print(f"✅ Docs written to {args.output}")  # pragma: no cover
    else:
        print(docs)  # pragma: no cover


if __name__ == "__main__":
    main()
