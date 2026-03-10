import ast
import os
from typing import List, Dict, Any, Optional

class CodeScanner:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def scan(self) -> List[Dict[str, Any]]:
        results = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    results.extend(self._scan_file(full_path))
        return results

    def _scan_file(self, filepath: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=filepath)

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    log_type = self._get_log_type(node)
                    if log_type:
                        findings.append({
                            "file": filepath,
                            "line": node.lineno,
                            "type": log_type,
                            "message_template": self._extract_message(node)
                        })
        except Exception:
            pass
        return findings

    def _get_log_type(self, node: ast.Call) -> Optional[str]:
        # Check for print()
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            return "print"

        # Check for logging.info(), logger.info(), etc.
        if isinstance(node.func, ast.Attribute):
            # Check if attr is info, debug, warning, error, critical
            if node.func.attr in ["info", "debug", "warning", "error", "critical", "log", "exception"]:
                return f"logging.{node.func.attr}"

        return None

    def _extract_message(self, node: ast.Call) -> str:
        # Try to extract the first argument as a string
        if node.args:
            arg = node.args[0]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                return arg.value
            elif isinstance(arg, ast.JoinedStr): # f-string
                parts = []
                for value in arg.values:
                    if isinstance(value, ast.Constant) and isinstance(value.value, str):
                        parts.append(value.value)
                    else:
                        parts.append("<VAR>")
                return "".join(parts)
            elif isinstance(arg, ast.BinOp): # "string" % var or "string" + var
                # Attempt to extract left side if it's a string
                if isinstance(arg.left, ast.Constant) and isinstance(arg.left.value, str):
                    return arg.left.value + "<VAR>"
                return "dynamic-expression"
        return "dynamic"
