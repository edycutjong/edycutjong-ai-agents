"""
Performance Profiler Agent — analyzes code for performance bottlenecks and optimization opportunities.
Usage: python main.py <source_file>
"""
import argparse, sys, os, re, ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Performance Profiler] Paste code to identify performance bottlenecks: N+1 queries, unnecessary loops, memory leaks, and optimization opportunities."


PERF_ISSUES = [
    (r"for .+ in .+:\s*\n\s*.+\.append\(", "Use list comprehension instead of loop+append"),
    (r"time\.sleep\(\d+\)", "Blocking sleep — consider async/await"),
    (r"\+\s*=\s*[\"']", "String concatenation in loop — use join() or StringIO"),
    (r"SELECT \* FROM", "SELECT * — fetch only needed columns"),
    (r"\.find\(.*\)\s+for", "List search in loop — consider set/dict for O(1) lookup"),
    (r"open\([^)]+\)(?!\s+as)", "File open without context manager (resource leak risk)"),
]


def main():
    parser = argparse.ArgumentParser(description="Profile code for performance issues")
    parser.add_argument("file", nargs="?", help="Source file to analyze")
    args = parser.parse_args()
    if not args.file:
        print("Performance Profiler Agent\nUsage: python main.py <source.py>")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)
    code = open(args.file).read()
    issues = [f"⚠️  {msg}" for pat, msg in PERF_ISSUES if re.search(pat, code, re.IGNORECASE)]

    # Check function complexity via AST
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                nested = sum(1 for n in ast.walk(node) if isinstance(n, (ast.For, ast.While, ast.ListComp)))
                if nested > 2:
                    issues.append(f"🔁 '{node.name}' has {nested} loops/comprehensions — potential O(n²)")
    except SyntaxError:
        pass

    print(f"\n⚡ Performance Report: {args.file}")
    for i in (issues or ["✅ No obvious performance issues detected."]):
        print(f"  {i}")

if __name__ == "__main__":
    main()
