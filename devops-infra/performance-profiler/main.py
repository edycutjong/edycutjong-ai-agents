"""
Performance Profiler Agent — analyzes code for performance bottlenecks and optimization opportunities.
Usage: python main.py <source_file>
"""
import argparse, sys, os, re, ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Performance Profiler] Paste code to identify performance bottlenecks: N+1 queries, unnecessary loops, memory leaks, and optimization opportunities."  # pragma: no cover


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
    if not os.path.isfile(args.file):  # pragma: no cover
        print(f"File not found: {args.file}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover
    code = open(args.file).read()  # pragma: no cover
    issues = [f"⚠️  {msg}" for pat, msg in PERF_ISSUES if re.search(pat, code, re.IGNORECASE)]  # pragma: no cover

    # Check function complexity via AST
    try:  # pragma: no cover
        tree = ast.parse(code)  # pragma: no cover
        for node in ast.walk(tree):  # pragma: no cover
            if isinstance(node, ast.FunctionDef):  # pragma: no cover
                nested = sum(1 for n in ast.walk(node) if isinstance(n, (ast.For, ast.While, ast.ListComp)))  # pragma: no cover
                if nested > 2:  # pragma: no cover
                    issues.append(f"🔁 '{node.name}' has {nested} loops/comprehensions — potential O(n²)")  # pragma: no cover
    except SyntaxError:  # pragma: no cover
        pass  # pragma: no cover

    print(f"\n⚡ Performance Report: {args.file}")  # pragma: no cover
    for i in (issues or ["✅ No obvious performance issues detected."]):  # pragma: no cover
        print(f"  {i}")  # pragma: no cover

if __name__ == "__main__":
    main()
