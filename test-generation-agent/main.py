"""
Test Generation Agent — generates unit tests for Python and JavaScript functions.
Usage: python main.py <source_file>
"""
import argparse, sys, os, re, ast


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Test Generation Agent] Paste a function or class definition to generate unit tests with happy path, edge cases, and error handling scenarios."


def extract_functions(code: str) -> list:
    try:
        tree = ast.parse(code)
        fns = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                params = [a.arg for a in node.args.args if a.arg != "self"]
                fns.append({"name": node.name, "params": params, "has_return": any(
                    isinstance(n, ast.Return) and n.value is not None for n in ast.walk(node))})
        return fns
    except SyntaxError:
        names = re.findall(r"^def (\w+)\s*\(([^)]*)\)", code, re.MULTILINE)
        return [{"name": n, "params": [p.strip() for p in ps.split(",") if p.strip()], "has_return": True} for n, ps in names]


def gen_tests(functions: list, module: str) -> str:
    lines = [f'import pytest\n# from {module} import {", ".join(f["name"] for f in functions[:3])}\n']
    for fn in functions:
        name = fn["name"]
        params = fn["params"]
        sample_args = ", ".join(["None"] * len(params))
        lines += [
            f"class Test{name.title().replace('_', '')}:",
            f"    def test_{name}_happy_path(self):",
            f"        # result = {name}({sample_args})",
            f"        # assert result is not None",
            f"        pass\n",
            f"    def test_{name}_edge_case_empty(self):",
            f"        # Test with empty/zero/None inputs",
            f"        pass\n",
            f"    def test_{name}_raises_on_invalid(self):",
            f"        # with pytest.raises(ValueError):",
            f"        #     {name}(invalid_input)",
            f"        pass\n",
        ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate unit test stubs from source code")
    parser.add_argument("file", nargs="?", help="Source file to generate tests for")
    parser.add_argument("--output", default="", help="Output test file")
    args = parser.parse_args()
    if not args.file:
        print("Test Generation Agent\nUsage: python main.py <source.py> [--output test_source.py]")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"File not found: {args.file}")
        sys.exit(1)
    code = open(args.file).read()
    fns = extract_functions(code)
    if not fns:
        print("No functions found.")
        sys.exit(0)
    module = os.path.splitext(os.path.basename(args.file))[0]
    tests = gen_tests(fns, module)
    if args.output:
        open(args.output, "w").write(tests)
        print(f"✅ Tests written to {args.output}")
    else:
        print(tests)

if __name__ == "__main__":
    main()
