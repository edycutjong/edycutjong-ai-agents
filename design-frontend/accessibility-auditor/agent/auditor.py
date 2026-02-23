"""Accessibility auditor — check HTML for WCAG compliance issues."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

@dataclass
class A11yIssue:
    rule: str
    severity: str  # error, warning, info
    element: str
    message: str
    def to_dict(self) -> dict: return self.__dict__.copy()

@dataclass
class A11yResult:
    total_issues: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    issues: list[A11yIssue] = field(default_factory=list)
    score: int = 100
    def to_dict(self) -> dict:
        return {"total_issues": self.total_issues, "errors": self.errors, "warnings": self.warnings, "score": self.score}

def audit_html(html: str) -> A11yResult:
    r = A11yResult()
    issues = []
    # Images without alt
    imgs_no_alt = re.findall(r'<img(?![^>]*\balt\s*=)[^>]*>', html, re.I)
    for img in imgs_no_alt:
        issues.append(A11yIssue("img-alt", "error", img[:60], "Image missing alt attribute"))
    # Empty alt on non-decorative images
    empty_alts = re.findall(r'<img[^>]*alt\s*=\s*""[^>]*>', html, re.I)
    for img in empty_alts:
        if 'role="presentation"' not in img.lower() and 'aria-hidden' not in img.lower():
            issues.append(A11yIssue("img-alt-empty", "warning", img[:60], "Image has empty alt (OK only if decorative)"))
    # Links without text
    empty_links = re.findall(r'<a[^>]*>\s*</a>', html, re.I)
    for link in empty_links:
        issues.append(A11yIssue("link-text", "error", link[:60], "Link has no accessible text"))
    # Missing lang attribute
    if re.search(r'<html', html, re.I) and not re.search(r'<html[^>]*\blang\s*=', html, re.I):
        issues.append(A11yIssue("html-lang", "error", "<html>", "Missing lang attribute on <html>"))
    # Missing page title
    if re.search(r'<head', html, re.I) and not re.search(r'<title[^>]*>.+</title>', html, re.I | re.DOTALL):
        issues.append(A11yIssue("page-title", "error", "<head>", "Page missing <title> element"))
    # Heading hierarchy
    headings = re.findall(r'<h(\d)', html, re.I)
    if headings:
        levels = [int(h) for h in headings]
        if levels[0] != 1:
            issues.append(A11yIssue("heading-order", "warning", f"<h{levels[0]}>", "First heading should be <h1>"))
        for i in range(1, len(levels)):
            if levels[i] > levels[i-1] + 1:
                issues.append(A11yIssue("heading-order", "warning", f"<h{levels[i]}>", f"Heading level skipped: h{levels[i-1]} → h{levels[i]}"))
    # Form inputs without labels
    inputs = re.findall(r'<input[^>]*>', html, re.I)
    for inp in inputs:
        if 'type="hidden"' in inp.lower() or 'type="submit"' in inp.lower(): continue
        inp_id = re.search(r'id\s*=\s*["\']([^"\']+)', inp)
        if inp_id:
            label_pattern = f'for\\s*=\\s*["\']{ re.escape(inp_id.group(1)) }["\']'
            if not re.search(label_pattern, html, re.I):
                if 'aria-label' not in inp.lower() and 'aria-labelledby' not in inp.lower():
                    issues.append(A11yIssue("input-label", "error", inp[:60], "Form input missing associated label"))
        elif 'aria-label' not in inp.lower():
            issues.append(A11yIssue("input-label", "warning", inp[:60], "Form input has no id or aria-label"))
    # Color contrast (basic — inline styles with small font)
    if re.search(r'font-size\s*:\s*[0-9]+px', html, re.I):
        sizes = re.findall(r'font-size\s*:\s*(\d+)px', html, re.I)
        for s in sizes:
            if int(s) < 12:
                issues.append(A11yIssue("text-size", "warning", f"font-size:{s}px", "Text smaller than 12px may be hard to read"))
    r.issues = issues
    r.total_issues = len(issues)
    r.errors = sum(1 for i in issues if i.severity == "error")
    r.warnings = sum(1 for i in issues if i.severity == "warning")
    r.infos = sum(1 for i in issues if i.severity == "info")
    r.score = max(0, 100 - (r.errors * 15) - (r.warnings * 5))
    return r

def format_result_markdown(r: A11yResult) -> str:
    emoji = "✅" if r.score >= 90 else "⚠️" if r.score >= 60 else "🔴"
    lines = [f"## Accessibility Audit {emoji}", f"**Score:** {r.score}/100 | **Errors:** {r.errors} | **Warnings:** {r.warnings}", ""]
    if not r.issues:
        lines.append("✅ No accessibility issues found!")
    else:
        for sev in ["error", "warning", "info"]:
            sev_issues = [i for i in r.issues if i.severity == sev]
            if sev_issues:
                icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[sev]
                lines.append(f"### {sev.title()}s ({len(sev_issues)})")
                for i in sev_issues:
                    lines.append(f"- {icon} **{i.rule}**: {i.message}")
                lines.append("")
    return "\n".join(lines)
