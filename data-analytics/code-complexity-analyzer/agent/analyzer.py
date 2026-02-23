"""Code complexity analyzer — analyze code for cyclomatic complexity and metrics."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

COMPLEXITY_KEYWORDS = {
    "python": r'\b(if|elif|else|for|while|except|with|and|or|assert|case)\b',
    "javascript": r'\b(if|else\s+if|else|for|while|do|switch|case|catch|&&|\|\||try)\b',
    "java": r'\b(if|else\s+if|else|for|while|do|switch|case|catch|&&|\|\|)\b',
    "go": r'\b(if|else\s+if|else|for|switch|case|select|&&|\|\|)\b',
}

@dataclass
class FunctionMetrics:
    name: str = ""; lines: int = 0; complexity: int = 1; params: int = 0

@dataclass
class ComplexityResult:
    total_lines: int = 0; code_lines: int = 0; comment_lines: int = 0; blank_lines: int = 0
    cyclomatic_complexity: int = 1; language: str = ""; functions: list[FunctionMetrics] = field(default_factory=list)
    grade: str = "A"; issues: list[str] = field(default_factory=list)
    def to_dict(self) -> dict: return {"lines": self.total_lines, "complexity": self.cyclomatic_complexity, "grade": self.grade}

def detect_language(code: str) -> str:
    if re.search(r'\bdef\b.*:', code) and "import" in code: return "python"
    if re.search(r'function\s+\w+\s*\(', code) or "const " in code or "let " in code: return "javascript"
    if "public class" in code or "void main" in code: return "java"
    if "func " in code and "package " in code: return "go"
    return "python"

def calculate_complexity(code: str, language: str = "") -> ComplexityResult:
    r = ComplexityResult()
    r.language = language or detect_language(code)
    lines = code.split("\n")
    r.total_lines = len(lines)
    for line in lines:
        stripped = line.strip()
        if not stripped: r.blank_lines += 1
        elif stripped.startswith(("#", "//", "/*", "*")): r.comment_lines += 1
        else: r.code_lines += 1
    pattern = COMPLEXITY_KEYWORDS.get(r.language, COMPLEXITY_KEYWORDS["python"])
    r.cyclomatic_complexity = 1 + len(re.findall(pattern, code))
    # Find functions
    if r.language == "python":
        for m in re.finditer(r'def\s+(\w+)\s*\(([^)]*)\)', code):
            f = FunctionMetrics(name=m.group(1), params=len([p for p in m.group(2).split(",") if p.strip()]))
            r.functions.append(f)
    # Grade
    c = r.cyclomatic_complexity
    if c <= 5: r.grade = "A"
    elif c <= 10: r.grade = "B"
    elif c <= 15: r.grade = "C"
    elif c <= 20: r.grade = "D"
    else: r.grade = "F"; r.issues.append("Extremely high complexity — consider refactoring")
    if r.total_lines > 500: r.issues.append("File is very long — consider splitting")
    return r

def get_maintainability_index(result: ComplexityResult) -> float:
    if result.code_lines == 0: return 100.0
    halstead = result.code_lines * 10  # simplified
    return max(0, round(171 - 5.2 * (halstead ** 0.5) - 0.23 * result.cyclomatic_complexity, 1))

def format_result_markdown(r: ComplexityResult) -> str:
    lines = [f"## Code Complexity 📊", f"**Language:** {r.language} | **Lines:** {r.total_lines} | **Cyclomatic:** {r.cyclomatic_complexity} | **Grade:** {r.grade}", ""]
    lines.append(f"- Code: {r.code_lines} | Comments: {r.comment_lines} | Blank: {r.blank_lines}")
    if r.functions:
        lines.append(f"\n**Functions detected:** {len(r.functions)}")
        for f in r.functions[:5]: lines.append(f"  - `{f.name}()` — {f.params} params")
    if r.issues:
        for i in r.issues: lines.append(f"⚠️ {i}")
    return "\n".join(lines)
