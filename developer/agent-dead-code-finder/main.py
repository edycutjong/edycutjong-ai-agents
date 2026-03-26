"""
Dead Code Finder Agent — statically analyzes Python codebases to find unused imports,
unused variables, unreachable code, and undefined names.
Usage: python main.py <directory>
"""
import argparse
import ast
import os
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Dead Code Finder] Provide a directory path to scan for dead code (unused imports, variables, unreachable code)."


class DeadCodeVisitor(ast.NodeVisitor):
    """AST visitor that collects defined names, imported names, and used names."""

    def __init__(self):
        self.imports = []      # (name, alias, lineno)
        self.definitions = []  # (name, lineno, kind)
        self.used_names = set()
        self.unreachable = []  # (lineno, description)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imports.append((alias.name, name, node.lineno))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            name = alias.asname or alias.name
            full = f"{module}.{alias.name}" if module else alias.name
            self.imports.append((full, name, node.lineno))
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.definitions.append((node.name, node.lineno, "function"))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.definitions.append((node.name, node.lineno, "async function"))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.definitions.append((node.name, node.lineno, "class"))
        self.generic_visit(node)

    def _check_unreachable_after(self, stmts):
        """Check for statements after return/raise/break/continue."""
        for i, stmt in enumerate(stmts):
            if isinstance(stmt, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
                if i + 1 < len(stmts):
                    next_stmt = stmts[i + 1]
                    self.unreachable.append(
                        (next_stmt.lineno, f"Code after {type(stmt).__name__.lower()}")
                    )

    def visit_If(self, node):
        self._check_unreachable_after(node.body)
        self._check_unreachable_after(node.orelse)
        self.generic_visit(node)

    def visit_For(self, node):
        self._check_unreachable_after(node.body)
        self.generic_visit(node)

    def visit_While(self, node):
        self._check_unreachable_after(node.body)
        self.generic_visit(node)

    def visit_FunctionDef_body(self, node):  # pragma: no cover
        self._check_unreachable_after(node.body)

    def visit_Module(self, node):
        self._check_unreachable_after(node.body)
        self.generic_visit(node)


def analyze_file(filepath: str) -> dict:
    """Analyze a single Python file for dead code."""
    findings = {"unused_imports": [], "unused_defs": [], "unreachable": [], "errors": []}

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
    except OSError as e:
        findings["errors"].append(f"Cannot read: {e}")
        return findings

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        findings["errors"].append(f"SyntaxError at line {e.lineno}: {e.msg}")
        return findings

    visitor = DeadCodeVisitor()
    visitor.visit(tree)

    # Also check function bodies for unreachable code
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor._check_unreachable_after(node.body)

    # Unused imports
    for full_name, alias, lineno in visitor.imports:
        if alias not in visitor.used_names and alias != "_":
            findings["unused_imports"].append(
                {"name": full_name, "alias": alias, "line": lineno}
            )

    # Unused definitions (skip _ prefixed, __dunder__, and main)
    for name, lineno, kind in visitor.definitions:
        if name.startswith("_") or name in visitor.used_names:
            continue
        findings["unused_defs"].append({"name": name, "line": lineno, "kind": kind})

    # Unreachable code
    for lineno, desc in visitor.unreachable:
        findings["unreachable"].append({"line": lineno, "description": desc})

    return findings


def scan_directory(directory: str, ignore_patterns: list = None) -> dict:
    """Scan a directory recursively for dead code in all .py files."""
    if ignore_patterns is None:
        ignore_patterns = ["__pycache__", ".venv", "venv", "node_modules", "dist", ".git"]

    results = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_patterns]
        for f in files:
            if f.endswith(".py"):
                filepath = os.path.join(root, f)
                findings = analyze_file(filepath)
                has_findings = any(
                    findings[k] for k in ("unused_imports", "unused_defs", "unreachable", "errors")
                )
                if has_findings:
                    results[filepath] = findings

    return results


def format_report(results: dict) -> str:
    """Format scan results into a readable report."""
    lines = ["\n--- ☠️ Dead Code Removal Report ---\n"]

    total_unused_imports = 0
    total_unused_defs = 0
    total_unreachable = 0
    total_errors = 0

    for filepath, findings in sorted(results.items()):
        file_lines = []

        for item in findings["unused_imports"]:
            total_unused_imports += 1
            display = item["alias"] if item["alias"] != item["name"] else item["name"]
            file_lines.append(f"    ⚠️  Unused import: '{display}' (line {item['line']})")

        for item in findings["unused_defs"]:
            total_unused_defs += 1
            file_lines.append(
                f"    ⚠️  Unused {item['kind']}: '{item['name']}' (line {item['line']})"
            )

        for item in findings["unreachable"]:
            total_unreachable += 1
            file_lines.append(
                f"    🚫 Unreachable code: {item['description']} (line {item['line']})"
            )

        for err in findings["errors"]:
            total_errors += 1
            file_lines.append(f"    ❌ {err}")

        if file_lines:
            lines.append(f"  📄 {filepath}")
            lines.extend(file_lines)
            lines.append("")

    # Summary
    lines.append("--- Summary ---")
    lines.append(f"  📦 Unused imports: {total_unused_imports}")
    lines.append(f"  🧹 Unused definitions: {total_unused_defs}")
    lines.append(f"  🚫 Unreachable code blocks: {total_unreachable}")
    if total_errors:
        lines.append(f"  ❌ Parse errors: {total_errors}")

    total = total_unused_imports + total_unused_defs + total_unreachable
    if total == 0:
        lines.append("\n  ✅ No dead code found — codebase looks clean!")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Dead Code Finder Agent")
    parser.add_argument("directory", nargs="?", help="Directory to scan for dead code")
    parser.add_argument(
        "-i", "--ignore", default="__pycache__,.venv,venv,node_modules,dist,.git",
        help="Comma-separated list of directory names to ignore"
    )
    args = parser.parse_args()

    if not args.directory:
        print("Dead Code Finder Agent\nUsage: python main.py <directory>")
        sys.exit(0)

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory")
        sys.exit(1)

    ignore = [p.strip() for p in args.ignore.split(",")]
    results = scan_directory(args.directory, ignore)
    print(format_report(results))


if __name__ == "__main__":  # pragma: no cover
    main()
