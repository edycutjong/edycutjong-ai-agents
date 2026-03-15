"""
Refactoring Agent — suggests refactoring improvements to improve code quality.
Usage: python main.py <source_file>
"""
import argparse, sys, os, re, ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Refactoring Agent] Paste code to get refactoring suggestions: extract functions, eliminate duplication, simplify conditions, and improve naming."


def main():
    parser = argparse.ArgumentParser(description="Suggest refactoring improvements")
    parser.add_argument("file", nargs="?", help="Source file to refactor")
    args = parser.parse_args()
    if not args.file:
        print("Refactoring Agent\nUsage: python main.py <source.py>")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)
    code = open(args.file).read()
    suggestions = []

    # Long functions
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                length = getattr(node, 'end_lineno', 0) - node.lineno
                if length > 40:
                    suggestions.append(f"📦 Extract: '{node.name}' is {length} lines — split into smaller functions")
                params = len(node.args.args)
                if params > 5:
                    suggestions.append(f"📋 '{node.name}' has {params} params — consider a config object or dataclass")
    except SyntaxError:
        suggestions.append("⚠️  Syntax error detected — fix before refactoring")

    # Duplicate patterns
    if re.search(r"if .+:\s*\n.+\n.*elif .+:\s*\n.+\n.*elif", code):
        suggestions.append("🔀 Long if/elif chain — consider dict dispatch or polymorphism")

    # Naming
    short_names = re.findall(r"\bdef ([a-z]{1,2})\s*\(", code)
    if short_names:
        suggestions.append(f"📝 Short function names: {short_names} — use descriptive names")

    print(f"\n🔧 Refactoring Suggestions: {args.file}")
    for s in (suggestions or ["✅ Code looks clean — no major refactoring needed."]):
        print(f"  {s}")

if __name__ == "__main__":
    main()
