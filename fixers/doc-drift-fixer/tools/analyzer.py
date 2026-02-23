import ast
from typing import Dict, List, Any

class CodeAnalyzer:
    """Analyzes Python code to extract structural information."""

    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyzes a Python file and returns its structure."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.analyze_code(code)
        except Exception as e:
            return {"error": str(e)}

    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Parses Python code and extracts definitions."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"error": f"SyntaxError: {e}"}

        definitions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                def_info = {
                    "type": type(node).__name__,
                    "name": node.name,
                    "lineno": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "args": [arg.arg for arg in node.args.args] if hasattr(node, 'args') else [],
                }

                # For classes, we could also look at methods, but for now flat list is okay
                # or maybe nested structure.
                # Let's keep it flat for now, but indicate parent if needed.

                definitions.append(def_info)

        return {"definitions": definitions}
