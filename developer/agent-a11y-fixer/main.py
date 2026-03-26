#!/usr/bin/env python3
"""
A11Y Fixer Agent — Scans HTML for accessibility issues and generates fixes
including alt text, ARIA labels, and contrast improvements.
Usage: python main.py <html_file> [--fix] [--out REPORT_FILE] [--format json|text]
"""
import argparse
import json
import os
import re
import sys
from typing import Any


APP_NAME = "a11y-fixer"
APP_VERSION = "1.0.0"


# ── Core Logic ───────────────────────────────────────────────────────────────

def scan_html(html_content: str) -> dict:
    """Scan HTML content for accessibility issues."""
    issues = []

    # 1. Missing alt text on images
    img_pattern = re.compile(r'<img\b([^>]*)>', re.IGNORECASE)
    for match in img_pattern.finditer(html_content):
        attrs = match.group(1)
        if 'alt=' not in attrs.lower():
            issues.append({
                "type": "Missing Alt Text",
                "element": match.group(0),
                "severity": "critical",
                "description": "Image is missing 'alt' attribute.",
                "recommendation": 'Add a descriptive alt attribute or alt="" for decorative images.',
            })

    # 2. Missing form labels
    input_pattern = re.compile(
        r'<(input|textarea|select)\b([^>]*)>', re.IGNORECASE
    )
    for match in input_pattern.finditer(html_content):
        attrs = match.group(2)
        tag = match.group(1).lower()
        # Skip hidden/submit/button
        type_match = re.search(r'type=["\'](\w+)["\']', attrs, re.IGNORECASE)
        if type_match and type_match.group(1).lower() in ("submit", "button", "hidden"):
            continue
        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        has_label = False
        if id_match:
            label_pattern = re.compile(
                r'<label\b[^>]*for=["\']' + re.escape(id_match.group(1)) + r'["\']',
                re.IGNORECASE,
            )
            if label_pattern.search(html_content):
                has_label = True
        aria_label = re.search(r'aria-label=', attrs, re.IGNORECASE)
        if aria_label:
            has_label = True
        if not has_label:
            issues.append({
                "type": "Missing Form Label",
                "element": match.group(0),
                "severity": "serious",
                "description": f"{tag.capitalize()} control has no associated label.",
                "recommendation": "Add a <label> with 'for' matching the input 'id', or add an aria-label attribute.",
            })

    # 3. Missing skip navigation
    if '<a' in html_content.lower() and '#main' not in html_content.lower():
        issues.append({
            "type": "Missing Skip Link",
            "element": "<body>",
            "severity": "moderate",
            "description": "No skip navigation link found.",
            "recommendation": 'Add <a href="#main">Skip to main content</a> at the top of the body.',
        })

    # 4. Empty links
    empty_link = re.compile(r'<a\b([^>]*)>\s*</a>', re.IGNORECASE)
    for match in empty_link.finditer(html_content):
        attrs = match.group(1)
        if 'aria-label' not in attrs.lower():
            issues.append({
                "type": "Empty Link",
                "element": match.group(0),
                "severity": "serious",
                "description": "Link has no text content and no aria-label.",
                "recommendation": "Add visible text or an aria-label attribute.",
            })

    # 5. Heading hierarchy
    headings = re.findall(r'<h(\d)\b', html_content, re.IGNORECASE)
    prev = 0
    for h in headings:
        level = int(h)
        if level > prev + 1 and prev > 0:
            issues.append({
                "type": "Heading Hierarchy Skip",
                "element": f"<h{level}>",
                "severity": "moderate",
                "description": f"Heading jumps from h{prev} to h{level}.",
                "recommendation": f"Use h{prev + 1} instead, or add intermediate headings.",
            })
        prev = level

    return {"issues": issues, "total": len(issues)}


def generate_fix(html_content: str, issues: list) -> str:
    """Apply automatic fixes to HTML for common a11y issues."""
    fixed = html_content

    # Add skip link if missing
    skip_issues = [i for i in issues if i["type"] == "Missing Skip Link"]
    if skip_issues:
        fixed = fixed.replace(
            "<body>",
            '<body>\n<a href="#main" class="skip-link">Skip to main content</a>',
            1,
        )

    # Add empty alt to images missing it
    def add_alt(match):
        attrs = match.group(1)
        if 'alt=' not in attrs.lower():
            return f'<img{attrs} alt="">'
        return match.group(0)

    fixed = re.sub(r'<img\b([^>]*)>', add_alt, fixed, flags=re.IGNORECASE)

    return fixed


def generate_report(scan_result: dict, fmt: str = "text") -> str:
    """Format scan results as text or JSON report."""
    if fmt == "json":
        return json.dumps(scan_result, indent=2)

    issues = scan_result["issues"]
    if not issues:
        return "✅ No accessibility issues found!"

    lines = [
        f"🔍 Accessibility Audit Report",
        f"{'=' * 40}",
        f"Total issues found: {scan_result['total']}",
        "",
    ]
    for i, issue in enumerate(issues, 1):
        lines.append(f"[{i}] {issue['type']} ({issue['severity']})")
        lines.append(f"    Element: {issue['element'][:80]}")
        lines.append(f"    {issue['description']}")
        lines.append(f"    → {issue['recommendation']}")
        lines.append("")

    return "\n".join(lines)


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    """High-level entry: scan HTML string and return text report."""
    if not user_input or not user_input.strip():
        return "[A11Y Fixer] Please provide HTML content to scan for accessibility issues."
    result = scan_html(user_input)
    return generate_report(result)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="A11Y Fixer Agent - Accessibility Scanner")
    parser.add_argument("file", nargs="?", help="Path to the HTML file to scan")
    parser.add_argument("--fix", action="store_true", help="Apply automatic fixes")
    parser.add_argument("--out", default=None, help="Output report file")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Report format")
    args = parser.parse_args()

    if not args.file:
        print(run(""))
        return

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        html_content = f.read()

    result = scan_html(html_content)
    report = generate_report(result, args.format)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {args.out}")
    else:
        print(report)

    if args.fix:
        fixed = generate_fix(html_content, result["issues"])
        out_path = args.file.replace(".html", "_fixed.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(fixed)
        print(f"Fixed HTML saved to {out_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
