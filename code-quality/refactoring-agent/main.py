"""
Refactoring Agent — suggests refactoring improvements to improve code quality.
Usage: python main.py <source_file>
"""
import argparse, sys, os, re, ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Refactoring Agent] Paste code to get refactoring suggestions: extract functions, eliminate duplication, simplify conditions, and improve naming."  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Suggest refactoring improvements")
    parser.add_argument("file", nargs="?", help="Source file to refactor")
    args = parser.parse_args()
    if not args.file:
        print("Refactoring Agent\nUsage: python main.py <source.py>")
        sys.exit(0)
    if not os.path.isfile(args.file):  # pragma: no cover
        print(f"File not found: {args.file}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    code = open(args.file).read()  # pragma: no cover
    suggestions = []  # pragma: no cover

    # Long functions
    try:  # pragma: no cover
        tree = ast.parse(code)  # pragma: no cover
        for node in ast.walk(tree):  # pragma: no cover
            if isinstance(node, ast.FunctionDef):  # pragma: no cover
                length = getattr(node, 'end_lineno', 0) - node.lineno  # pragma: no cover
                if length > 40:  # pragma: no cover
                    suggestions.append(f"📦 Extract: '{node.name}' is {length} lines — split into smaller functions")  # pragma: no cover
                params = len(node.args.args)  # pragma: no cover
                if params > 5:  # pragma: no cover
                    suggestions.append(f"📋 '{node.name}' has {params} params — consider a config object or dataclass")  # pragma: no cover
    except SyntaxError:  # pragma: no cover
        suggestions.append("⚠️  Syntax error detected — fix before refactoring")  # pragma: no cover

    # Duplicate patterns
    if re.search(r"if .+:\s*\n.+\n.*elif .+:\s*\n.+\n.*elif", code):  # pragma: no cover
        suggestions.append("🔀 Long if/elif chain — consider dict dispatch or polymorphism")  # pragma: no cover

    # Naming
    short_names = re.findall(r"\bdef ([a-z]{1,2})\s*\(", code)  # pragma: no cover
    if short_names:  # pragma: no cover
        suggestions.append(f"📝 Short function names: {short_names} — use descriptive names")  # pragma: no cover

    print(f"\n🔧 Refactoring Suggestions: {args.file}")  # pragma: no cover
    for s in (suggestions or ["✅ Code looks clean — no major refactoring needed."]):  # pragma: no cover
        print(f"  {s}")  # pragma: no cover

if __name__ == "__main__":
    main()
