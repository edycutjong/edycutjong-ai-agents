"""
Test Case Generator Agent — analyzes function signatures and generates unit tests.
Usage: python main.py <source_file.py>
"""
import argparse
import ast
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Test Case Generator] Provide a source file to generate comprehensive unit test cases."


def extract_functions(source: str) -> list:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = []
            for arg in node.args.args:
                if arg.arg == "self":
                    continue
                annotation = None
                if arg.annotation and isinstance(arg.annotation, ast.Name):
                    annotation = arg.annotation.id
                params.append({"name": arg.arg, "type": annotation})
            has_return = any(isinstance(n, ast.Return) and n.value is not None
                            for n in ast.walk(node))
            functions.append({
                "name": node.name, "params": params,
                "has_return": has_return, "is_async": isinstance(node, ast.AsyncFunctionDef),
                "lineno": node.lineno
            })
    return functions


TYPE_VALUES = {
    "str": ('""', '"hello"', '"a" * 1000', 'None'),
    "int": ("0", "1", "-1", "999999"),
    "float": ("0.0", "1.5", "-1.0", "float('inf')"),
    "bool": ("True", "False"),
    "list": ("[]", "[1, 2, 3]", 'None'),
    "dict": ("{}", '{"key": "val"}', 'None'),
    None: ('""', "0", "None", "[]"),
}


def generate_test_cases(func: dict) -> list:
    tests = []
    name = func["name"]
    params = func["params"]

    # Happy path
    args = ", ".join(TYPE_VALUES.get(p["type"], TYPE_VALUES[None])[1] for p in params)
    tests.append({"name": f"test_{name}_happy_path", "args": args, "kind": "happy"})

    # Empty/zero values
    args = ", ".join(TYPE_VALUES.get(p["type"], TYPE_VALUES[None])[0] for p in params)
    tests.append({"name": f"test_{name}_empty_input", "args": args, "kind": "edge"})

    # None handling
    if params:
        args = ", ".join("None" for _ in params)
        tests.append({"name": f"test_{name}_none_input", "args": args, "kind": "error"})

    return tests


def generate_test_file(functions: list, module_name: str) -> str:
    lines = [f'"""Auto-generated tests for {module_name}"""\n',
             "import pytest",
             f"from {module_name} import {', '.join(f['name'] for f in functions)}\n\n"]

    for func in functions:
        cases = generate_test_cases(func)
        for case in cases:
            prefix = "async " if func["is_async"] else ""
            decorator = "@pytest.mark.asyncio\n" if func["is_async"] else ""
            await_kw = "await " if func["is_async"] else ""
            lines.append(f"{decorator}def {case['name']}():")
            if case["kind"] == "error":
                lines.append(f"    with pytest.raises(Exception):")
                lines.append(f"        {await_kw}{func['name']}({case['args']})")
            elif func["has_return"]:
                lines.append(f"    result = {await_kw}{func['name']}({case['args']})")
                lines.append(f"    assert result is not None")
            else:
                lines.append(f"    {await_kw}{func['name']}({case['args']})  # should not raise")
            lines.append("")

    return "\n".join(lines)


def format_preview(functions: list) -> str:
    lines = [f"🧪 Test Generator — {len(functions)} function(s) found\n"]
    for f in functions:
        params = ", ".join(f"{p['name']}: {p['type'] or 'Any'}" for p in f["params"])
        lines.append(f"  📌 {f['name']}({params}) → {len(generate_test_cases(f))} test(s)")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Test Case Generator Agent")
    parser.add_argument("file", nargs="?", help="Python source file")
    parser.add_argument("--output", default="", help="Output test file path")
    args = parser.parse_args()
    if not args.file:
        print("Test Case Generator Agent\nUsage: python main.py <source.py>")
        sys.exit(0)
    source = open(args.file).read()
    functions = extract_functions(source)
    if not functions:
        print("No functions found.")
        sys.exit(0)
    print(format_preview(functions))
    if args.output:
        module = os.path.splitext(os.path.basename(args.file))[0]
        test_code = generate_test_file(functions, module)
        with open(args.output, "w") as f:
            f.write(test_code)
        print(f"\n✅ Written to {args.output}")


if __name__ == "__main__":
    main()
