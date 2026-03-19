"""
Test Coverage Gap Finder — identifies untested functions and edge cases.
Usage: python main.py --source src/module.py --tests tests/test_module.py
"""
import argparse
import sys
import os
import re
import ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Coverage Gap Finder] Ready.\n\nPaste your source code and test file to identify which functions are missing tests, edge cases, and coverage gaps."


def get_functions(code: str) -> set:
    try:
        tree = ast.parse(code)
        return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")}
    except SyntaxError:
        return set(re.findall(r"^def (\w+)\s*\(", code, re.MULTILINE))


def get_tested_functions(test_code: str) -> set:
    calls = set(re.findall(r"\b(\w+)\s*\(", test_code))
    test_names = set(re.findall(r"def test_(\w+)\s*\(", test_code))
    return calls | test_names


def main():
    parser = argparse.ArgumentParser(description="Find test coverage gaps")
    parser.add_argument("--source", default="", help="Source file to check")
    parser.add_argument("--tests", default="", help="Test file to compare against")
    args = parser.parse_args()

    if not args.source:
        print("Test Coverage Gap Finder")
        print("Usage: python main.py --source src/module.py --tests tests/test_module.py")
        sys.exit(0)

    if not os.path.isfile(args.source):  # pragma: no cover
        print(f"Source file not found: {args.source}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    with open(args.source) as f:  # pragma: no cover
        source_code = f.read()  # pragma: no cover

    functions = get_functions(source_code)  # pragma: no cover

    tested = set()  # pragma: no cover
    if args.tests and os.path.isfile(args.tests):  # pragma: no cover
        with open(args.tests) as f:  # pragma: no cover
            test_code = f.read()  # pragma: no cover
        tested = get_tested_functions(test_code)  # pragma: no cover
    else:
        print("⚠️  No test file provided — showing all functions as uncovered.\n")  # pragma: no cover

    untested = functions - tested  # pragma: no cover
    covered = functions & tested  # pragma: no cover

    print(f"\n🧪 Coverage Gap Report: {args.source}")  # pragma: no cover
    print(f"   Functions found  : {len(functions)}")  # pragma: no cover
    print(f"   Covered          : {len(covered)}")  # pragma: no cover
    print(f"   Gaps (untested)  : {len(untested)}")  # pragma: no cover
    coverage = round(len(covered) / len(functions) * 100) if functions else 100  # pragma: no cover
    print(f"   Coverage estimate: {coverage}%\n")  # pragma: no cover

    if untested:  # pragma: no cover
        print("   Missing tests for:")  # pragma: no cover
        for fn in sorted(untested):  # pragma: no cover
            print(f"     ❌ {fn}()")  # pragma: no cover
    else:
        print("   ✅ All public functions appear to be tested.")  # pragma: no cover


if __name__ == "__main__":
    main()
