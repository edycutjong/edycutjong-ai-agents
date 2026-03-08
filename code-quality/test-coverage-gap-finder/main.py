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

    if not os.path.isfile(args.source):
        print(f"Source file not found: {args.source}")
        sys.exit(1)

    with open(args.source) as f:
        source_code = f.read()

    functions = get_functions(source_code)

    tested = set()
    if args.tests and os.path.isfile(args.tests):
        with open(args.tests) as f:
            test_code = f.read()
        tested = get_tested_functions(test_code)
    else:
        print("⚠️  No test file provided — showing all functions as uncovered.\n")

    untested = functions - tested
    covered = functions & tested

    print(f"\n🧪 Coverage Gap Report: {args.source}")
    print(f"   Functions found  : {len(functions)}")
    print(f"   Covered          : {len(covered)}")
    print(f"   Gaps (untested)  : {len(untested)}")
    coverage = round(len(covered) / len(functions) * 100) if functions else 100
    print(f"   Coverage estimate: {coverage}%\n")

    if untested:
        print("   Missing tests for:")
        for fn in sorted(untested):
            print(f"     ❌ {fn}()")
    else:
        print("   ✅ All public functions appear to be tested.")


if __name__ == "__main__":
    main()
