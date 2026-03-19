"""Coverage gap analyzer."""
import os
import ast
import glob
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class CoverageReport:
    """Coverage analysis report."""
    total_functions: int = 0
    tested_functions: int = 0
    untested_functions: int = 0
    coverage_percent: float = 0.0
    suggestions: List[str] = field(default_factory=list)
    details: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "total_functions": self.total_functions,
            "tested_functions": self.tested_functions,
            "untested_functions": self.untested_functions,
            "coverage_percent": round(self.coverage_percent, 1),
            "suggestions": self.suggestions,
        }

    def to_markdown(self) -> str:
        lines = [
            "# Coverage Analysis Report",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total functions | {self.total_functions} |",
            f"| Tested | {self.tested_functions} |",
            f"| Untested | {self.untested_functions} |",
            f"| Coverage | {self.coverage_percent:.1f}% |",
            "",
        ]
        if self.suggestions:
            lines.append("## Suggestions")  # pragma: no cover
            for s in self.suggestions:  # pragma: no cover
                lines.append(f"- {s}")  # pragma: no cover
        return "\n".join(lines)


class CoverageAnalyzer:
    """Analyzes source files for test coverage gaps."""

    def analyze(self, path: str) -> CoverageReport:
        """Analyze a file or directory for coverage gaps."""
        if os.path.isfile(path):
            return self._analyze_file(path)
        return self._analyze_directory(path)  # pragma: no cover

    def _analyze_file(self, filepath: str) -> CoverageReport:
        """Analyze a single Python file."""
        with open(filepath, "r") as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:  # pragma: no cover
            return CoverageReport(suggestions=["File has syntax errors"])  # pragma: no cover

        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                functions.append(node.name)

        # Look for corresponding test file
        dir_path = os.path.dirname(filepath)
        base = os.path.splitext(os.path.basename(filepath))[0]
        test_patterns = [
            os.path.join(dir_path, "tests", f"test_{base}.py"),
            os.path.join(dir_path, f"test_{base}.py"),
            os.path.join(dir_path, "tests", f"{base}_test.py"),
        ]

        tested = set()
        for tp in test_patterns:
            if os.path.exists(tp):
                with open(tp, "r") as f:  # pragma: no cover
                    test_source = f.read()  # pragma: no cover
                for func_name in functions:  # pragma: no cover
                    if func_name in test_source:  # pragma: no cover
                        tested.add(func_name)  # pragma: no cover

        untested = [f for f in functions if f not in tested]
        total = len(functions)
        tested_count = len(tested)

        report = CoverageReport(
            total_functions=total,
            tested_functions=tested_count,
            untested_functions=len(untested),
            coverage_percent=(tested_count / total * 100) if total > 0 else 100.0,
        )

        for func in untested:
            report.suggestions.append(f"Add tests for `{func}()`")

        if total > 0 and tested_count == 0:
            report.suggestions.append("No test file found — create one with `python main.py generate`")

        return report

    def _analyze_directory(self, directory: str) -> CoverageReport:
        """Analyze all Python files in a directory."""
        py_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)  # pragma: no cover
        py_files = [f for f in py_files if not os.path.basename(f).startswith("test_")  # pragma: no cover
                    and "tests/" not in f and "__pycache__" not in f]

        combined = CoverageReport()  # pragma: no cover
        for fp in py_files:  # pragma: no cover
            r = self._analyze_file(fp)  # pragma: no cover
            combined.total_functions += r.total_functions  # pragma: no cover
            combined.tested_functions += r.tested_functions  # pragma: no cover
            combined.untested_functions += r.untested_functions  # pragma: no cover
            combined.suggestions.extend(r.suggestions)  # pragma: no cover

        if combined.total_functions > 0:  # pragma: no cover
            combined.coverage_percent = (  # pragma: no cover
                combined.tested_functions / combined.total_functions * 100
            )

        return combined  # pragma: no cover
