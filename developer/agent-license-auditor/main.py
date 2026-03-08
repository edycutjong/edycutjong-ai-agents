"""
License Auditor Agent — scans dependencies and reports license types, flags risky ones.
Usage: python main.py [--requirements requirements.txt] [--package-json package.json]
"""
import argparse
import sys
import re
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[License Auditor] Ready.\n\nPaste your requirements.txt, package.json dependencies, or a list of packages to get a license audit with risk flags."


RISKY_LICENSES = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0", "SSPL"}
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense", "CC0-1.0"}

KNOWN_LICENSES = {
    "requests": "Apache-2.0", "flask": "BSD-3-Clause", "django": "BSD-3-Clause",
    "numpy": "BSD-3-Clause", "pandas": "BSD-3-Clause", "pytest": "MIT",
    "sqlalchemy": "MIT", "pydantic": "MIT", "fastapi": "MIT",
    "react": "MIT", "lodash": "MIT", "express": "MIT",
    "mongodb": "SSPL", "elasticsearch": "SSPL", "redis": "BSD-3-Clause",
    "streamlit": "Apache-2.0", "openai": "MIT", "langchain": "MIT",
}


def parse_requirements(text: str) -> list:
    packages = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            name = re.split(r"[>=<!=\[]", line)[0].strip().lower()
            if name:
                packages.append(name)
    return packages


def audit_packages(packages: list) -> None:
    print(f"{'Package':<30} {'License':<20} {'Risk'}")
    print("-" * 60)
    unknown = []
    for pkg in packages:
        license_id = KNOWN_LICENSES.get(pkg.lower(), "Unknown")
        if license_id == "Unknown":
            unknown.append(pkg)
            risk = "❓ Unknown"
        elif license_id in RISKY_LICENSES:
            risk = "⚠️  Copyleft — review required"
        elif license_id in PERMISSIVE:
            risk = "✅ Permissive"
        else:
            risk = "ℹ️  Review"
        print(f"{pkg:<30} {license_id:<20} {risk}")

    if unknown:
        print(f"\n⚠️  {len(unknown)} package(s) with unknown licenses — check manually: {', '.join(unknown[:10])}")


def main():
    parser = argparse.ArgumentParser(description="Audit dependency licenses")
    parser.add_argument("--requirements", default="", help="Path to requirements.txt")
    parser.add_argument("--packages", nargs="+", help="List of package names to audit")
    args = parser.parse_args()

    if args.requirements:
        if not os.path.isfile(args.requirements):
            print(f"File not found: {args.requirements}")
            sys.exit(1)
        with open(args.requirements) as f:
            packages = parse_requirements(f.read())
    elif args.packages:
        packages = args.packages
    else:
        print("License Auditor Agent")
        print("Usage: python main.py --requirements requirements.txt")
        print("       python main.py --packages flask requests pandas")
        sys.exit(0)

    print(f"\n📋 License Audit Report ({len(packages)} packages)\n")
    audit_packages(packages)


if __name__ == "__main__":
    main()
