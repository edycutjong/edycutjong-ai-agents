"""Code explainer — analyze and explain code snippets."""
from __future__ import annotations
import re, ast
from dataclasses import dataclass, field

@dataclass
class CodeAnalysis:
    language: str = ""
    lines: int = 0
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    comments: int = 0
    complexity: str = "low"  # low, medium, high
    concepts: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return self.__dict__.copy()

LANGUAGE_HINTS = {
    "python": [r"\bdef\b", r"\bimport\b", r"\bclass\b.*:", r"print\(", r"self\.", r"__\w+__"],
    "javascript": [r"\bfunction\b", r"\bconst\b", r"\blet\b", r"=>", r"console\.", r"require\("],
    "typescript": [r"\binterface\b", r":\s*(string|number|boolean)", r"\btype\b\s+\w+"],
    "html": [r"<html", r"<div", r"<head", r"<!DOCTYPE"],
    "css": [r"\{[^}]*:[^}]*\}", r"@media", r"\.[\w-]+\s*\{"],
    "sql": [r"\bSELECT\b", r"\bFROM\b", r"\bINSERT\b", r"\bCREATE TABLE\b"],
}

def detect_language(code: str) -> str:
    scores = {}
    for lang, patterns in LANGUAGE_HINTS.items():
        scores[lang] = sum(1 for p in patterns if re.search(p, code, re.I))
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unknown"

def analyze_python(code: str) -> CodeAnalysis:
    analysis = CodeAnalysis(language="python", lines=len(code.strip().split("\n")))
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef): analysis.functions.append(node.name)
            elif isinstance(node, ast.AsyncFunctionDef): analysis.functions.append(f"async {node.name}")
            elif isinstance(node, ast.ClassDef): analysis.classes.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names: analysis.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module: analysis.imports.append(node.module)
    except SyntaxError: pass
    analysis.comments = sum(1 for line in code.split("\n") if line.strip().startswith("#"))
    # Complexity
    nested = len(re.findall(r"\b(if|for|while|try|with)\b", code))
    analysis.complexity = "high" if nested > 10 else "medium" if nested > 4 else "low"
    # Concepts
    if analysis.classes: analysis.concepts.append("OOP")
    if "async" in code or "await" in code: analysis.concepts.append("Async")
    if "lambda" in code: analysis.concepts.append("Lambda")
    if any("comprehension" in str(code) or "[" in line and "for" in line for line in code.split("\n")): analysis.concepts.append("Comprehensions")
    if "decorator" in code or re.search(r"@\w+", code): analysis.concepts.append("Decorators")
    return analysis

def analyze_code(code: str, language: str | None = None) -> CodeAnalysis:
    if not language: language = detect_language(code)
    if language == "python": return analyze_python(code)
    # Generic analysis
    analysis = CodeAnalysis(language=language, lines=len(code.strip().split("\n")))
    analysis.functions = re.findall(r"\bfunction\s+(\w+)", code)
    analysis.classes = re.findall(r"\bclass\s+(\w+)", code)
    analysis.comments = len(re.findall(r"//.*|/\*[\s\S]*?\*/|#.*", code))
    return analysis

def explain_code(code: str, language: str | None = None) -> str:
    analysis = analyze_code(code, language)
    lines = [f"## Code Analysis ({analysis.language})", f"**Lines:** {analysis.lines} | **Complexity:** {analysis.complexity}", ""]
    if analysis.imports:
        lines.append("### Imports")
        for imp in analysis.imports: lines.append(f"- `{imp}`")
        lines.append("")
    if analysis.classes:
        lines.append("### Classes")
        for cls in analysis.classes: lines.append(f"- `{cls}`")
        lines.append("")
    if analysis.functions:
        lines.append("### Functions")
        for fn in analysis.functions: lines.append(f"- `{fn}()`")
        lines.append("")
    if analysis.concepts:
        lines.append("### Concepts Used")
        for c in analysis.concepts: lines.append(f"- {c}")
    return "\n".join(lines)
