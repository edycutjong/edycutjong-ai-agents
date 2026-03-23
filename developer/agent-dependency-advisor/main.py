"""
Dependency Advisor Agent — analyzes package.json/requirements.txt and recommends
updates, alternatives, and security fixes.
Usage: python main.py <package.json|requirements.txt>
"""
import argparse
import json
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Dependency Advisor] Provide a package.json or requirements.txt to get dependency advice."


KNOWN_DEPRECATED = {
    "request": "Use 'got' or 'node-fetch' instead",
    "moment": "Use 'date-fns' or 'dayjs' instead",
    "tslint": "Use 'eslint' with @typescript-eslint instead",
    "uglify-js": "Use 'terser' instead",
    "node-sass": "Use 'sass' (dart-sass) instead",
    "bower": "Use npm/yarn directly",
}

SECURITY_NOTES = {
    "lodash": "Ensure version >= 4.17.21 (prototype pollution)",
    "minimist": "Ensure version >= 1.2.6 (prototype pollution)",
    "jsonwebtoken": "Ensure version >= 9.0.0 (algorithm confusion)",
}


def analyze_npm(data: dict) -> list:
    findings = []
    for section in ["dependencies", "devDependencies"]:
        deps = data.get(section, {})
        for pkg, ver in deps.items():
            pkg_lower = pkg.lower()
            if pkg_lower in KNOWN_DEPRECATED:
                findings.append({"package": pkg, "type": "DEPRECATED",
                                 "advice": KNOWN_DEPRECATED[pkg_lower], "severity": "WARNING"})
            if pkg_lower in SECURITY_NOTES:
                findings.append({"package": pkg, "type": "SECURITY",
                                 "advice": SECURITY_NOTES[pkg_lower], "severity": "HIGH"})
            if ver.startswith("*") or ver == "latest":
                findings.append({"package": pkg, "type": "PINNING",
                                 "advice": "Pin to specific version — '*' and 'latest' are risky",
                                 "severity": "WARNING"})
    return findings


def analyze_pip(content: str) -> list:
    findings = []
    for line in content.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([a-zA-Z0-9_-]+)", line)
        if match:
            pkg = match.group(1)
            if "==" not in line and ">=" not in line and "<" not in line:
                findings.append({"package": pkg, "type": "PINNING",
                                 "advice": "Pin version with == for reproducible builds",
                                 "severity": "INFO"})
    return findings


def format_report(findings: list) -> str:
    if not findings:
        return "✅ All dependencies look good — no issues found."
    lines = [f"📋 Dependency Advisor Report — {len(findings)} finding(s)\n"]
    for f in findings:
        icons = {"HIGH": "🔴", "WARNING": "🟡", "INFO": "🔵"}
        icon = icons.get(f["severity"], "⚪")
        lines.append(f"  {icon} [{f['type']}] {f['package']}: {f['advice']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Dependency Advisor Agent")
    parser.add_argument("file", nargs="?", help="package.json or requirements.txt")
    args = parser.parse_args()
    if not args.file:
        print("Dependency Advisor Agent\nUsage: python main.py <package.json|requirements.txt>")
        sys.exit(0)
    if not os.path.isfile(args.file):
        print(f"Error: {args.file} not found")
        sys.exit(1)
    content = open(args.file).read()
    if args.file.endswith(".json"):
        findings = analyze_npm(json.loads(content))
    else:
        findings = analyze_pip(content)
    print(format_report(findings))


if __name__ == "__main__":
    main()
