import ast
import os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DocTarget:
    filepath: str
    name: str
    lineno: int
    node_type: str  # 'function', 'class', 'async_function'
    code_snippet: str

class CodeParser:
    def __init__(self):
        pass

    def scan_directory(self, directory: str) -> List[DocTarget]:
        targets = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    targets.extend(self.find_missing_docstrings(filepath))
        return targets

    def find_missing_docstrings(self, filepath: str) -> List[DocTarget]:
        targets = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)
            lines = source.splitlines()

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        # Calculate start and end lines for the snippet
                        start_line = node.lineno - 1
                        end_line = node.end_lineno
                        snippet = "\n".join(lines[start_line:end_line])

                        node_type = "function"
                        if isinstance(node, ast.AsyncFunctionDef):
                            node_type = "async_function"
                        elif isinstance(node, ast.ClassDef):
                            node_type = "class"

                        targets.append(DocTarget(
                            filepath=filepath,
                            name=node.name,
                            lineno=node.lineno,
                            node_type=node_type,
                            code_snippet=snippet
                        ))
        except Exception as e:
            # In a real app, log this error
            print(f"Error parsing {filepath}: {e}")
            pass

        return targets
