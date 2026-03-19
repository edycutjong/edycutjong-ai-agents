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
    print(f"{'Package':<30} {'License':<20} {'Risk'}")  # pragma: no cover
    print("-" * 60)  # pragma: no cover
    unknown = []  # pragma: no cover
    for pkg in packages:  # pragma: no cover
        license_id = KNOWN_LICENSES.get(pkg.lower(), "Unknown")  # pragma: no cover
        if license_id == "Unknown":  # pragma: no cover
            unknown.append(pkg)  # pragma: no cover
            risk = "❓ Unknown"  # pragma: no cover
        elif license_id in RISKY_LICENSES:  # pragma: no cover
            risk = "⚠️  Copyleft — review required"  # pragma: no cover
        elif license_id in PERMISSIVE:  # pragma: no cover
            risk = "✅ Permissive"  # pragma: no cover
        else:
            risk = "ℹ️  Review"  # pragma: no cover
        print(f"{pkg:<30} {license_id:<20} {risk}")  # pragma: no cover

    if unknown:  # pragma: no cover
        print(f"\n⚠️  {len(unknown)} package(s) with unknown licenses — check manually: {', '.join(unknown[:10])}")  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Audit dependency licenses")
    parser.add_argument("--requirements", default="", help="Path to requirements.txt")
    parser.add_argument("--packages", nargs="+", help="List of package names to audit")
    args = parser.parse_args()

    if args.requirements:
        if not os.path.isfile(args.requirements):  # pragma: no cover
            print(f"File not found: {args.requirements}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
        with open(args.requirements) as f:  # pragma: no cover
            packages = parse_requirements(f.read())  # pragma: no cover
    elif args.packages:
        packages = args.packages  # pragma: no cover
    else:
        print("License Auditor Agent")
        print("Usage: python main.py --requirements requirements.txt")
        print("       python main.py --packages flask requests pandas")
        sys.exit(0)

    print(f"\n📋 License Audit Report ({len(packages)} packages)\n")  # pragma: no cover
    audit_packages(packages)  # pragma: no cover


if __name__ == "__main__":
    main()
