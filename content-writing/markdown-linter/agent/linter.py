"""Markdown linter — check markdown files for common issues and best practices."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class LintIssue:
    line: int = 0; rule: str = ""; message: str = ""; severity: str = "warning"

@dataclass
class LintResult:
    issues: list[LintIssue] = field(default_factory=list)
    warnings: int = 0; errors: int = 0; total_lines: int = 0
    is_valid: bool = True
    def to_dict(self) -> dict: return {"warnings": self.warnings, "errors": self.errors, "total_lines": self.total_lines, "is_valid": self.is_valid}

RULES = {
    "no-trailing-spaces": "Trailing whitespace",
    "no-multiple-blanks": "Multiple consecutive blank lines",
    "heading-style": "Heading should have space after #",
    "no-bare-urls": "Bare URL should be wrapped in angle brackets or markdown link",
    "list-marker": "List items should use consistent markers",
    "heading-increment": "Heading levels should not skip levels",
    "no-duplicate-heading": "Duplicate heading detected",
}

def lint_markdown(text: str) -> LintResult:
    r = LintResult()
    lines = text.split("\n")
    r.total_lines = len(lines)
    prev_blank = False; headings = []; heading_levels = []; heading_texts = []
    for i, line in enumerate(lines, 1):
        # Trailing spaces
        if line.rstrip("\n") != line.rstrip():
            r.issues.append(LintIssue(i, "no-trailing-spaces", "Trailing whitespace", "warning"))
        # Multiple blank lines
        is_blank = not line.strip()
        if is_blank and prev_blank:
            r.issues.append(LintIssue(i, "no-multiple-blanks", "Multiple consecutive blank lines", "warning"))
        prev_blank = is_blank
        # Heading style: #text without space
        m = re.match(r'^(#{1,6})([^\s#])', line)
        if m:
            r.issues.append(LintIssue(i, "heading-style", f"Missing space after {m.group(1)}", "error"))
        # Heading increment
        hm = re.match(r'^(#{1,6})\s+(.+)', line)
        if hm:
            level = len(hm.group(1)); text_h = hm.group(2).lower()
            if heading_levels and level > heading_levels[-1] + 1:
                r.issues.append(LintIssue(i, "heading-increment", f"Heading skipped from h{heading_levels[-1]} to h{level}", "warning"))
            heading_levels.append(level)
            if text_h in heading_texts:
                r.issues.append(LintIssue(i, "no-duplicate-heading", f"Duplicate heading: {hm.group(2)}", "warning"))
            heading_texts.append(text_h)
        # Bare URLs
        if re.search(r'(?<!\[)\bhttps?://\S+(?!\])', line) and not re.search(r'^\s*[-*]?\s*https?://', line):
            r.issues.append(LintIssue(i, "no-bare-urls", "Bare URL found", "warning"))
    r.warnings = sum(1 for i in r.issues if i.severity == "warning")
    r.errors = sum(1 for i in r.issues if i.severity == "error")
    r.is_valid = r.errors == 0
    return r

def get_issues_by_rule(result: LintResult) -> dict:
    by_rule = {}
    for issue in result.issues:
        by_rule.setdefault(issue.rule, []).append(issue)
    return by_rule

def format_result_markdown(r: LintResult) -> str:
    emoji = "✅" if r.is_valid else "❌"
    lines = [f"## Markdown Lint {emoji}", f"**Lines:** {r.total_lines} | **Errors:** {r.errors} | **Warnings:** {r.warnings}", ""]
    for issue in r.issues[:20]:
        ico = "❌" if issue.severity == "error" else "⚠️"
        lines.append(f"{ico} Line {issue.line}: [{issue.rule}] {issue.message}")
    return "\n".join(lines)
