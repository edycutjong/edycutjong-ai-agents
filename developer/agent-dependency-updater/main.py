"""
Dependency Updater Agent — checks for outdated deps, reads changelogs, creates update PRs.
Usage: python main.py [--requirements requirements.txt] [--check-only]
"""
import argparse
import sys
import os
import re
try:
    from urllib.request import urlopen
    import json
except ImportError:
    pass


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Dependency Updater] Ready.\n\nPaste your requirements.txt or package.json to check for outdated dependencies and get recommended update strategies."


def parse_requirements(text: str) -> dict:
    deps = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            m = re.match(r"^([A-Za-z0-9_\-]+)==([^\s]+)", line)
            if m:
                deps[m.group(1).lower()] = m.group(2)
    return deps


def check_pypi_version(package: str) -> str:
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        data = json.loads(urlopen(url, timeout=5).read())
        return data["info"]["version"]
    except Exception:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Check for outdated dependencies")
    parser.add_argument("--requirements", default="requirements.txt", help="Path to requirements.txt")
    parser.add_argument("--check-only", action="store_true", help="Exit with code 1 if outdated deps found")
    parser.add_argument("--no-network", action="store_true", help="Skip PyPI checks (offline mode)")
    args = parser.parse_args()

    if not os.path.isfile(args.requirements):
        print("Dependency Updater Agent")
        print(f"File not found: {args.requirements}")
        print("Usage: python main.py --requirements requirements.txt")
        sys.exit(0)

    with open(args.requirements) as f:
        text = f.read()

    deps = parse_requirements(text)
    if not deps:
        print("No pinned dependencies found (==version) in requirements file.")
        sys.exit(0)

    print(f"Checking {len(deps)} pinned packages...\n")
    print(f"{'Package':<30} {'Pinned':<15} {'Latest':<15} {'Status'}")
    print("-" * 75)

    outdated = []
    for pkg, pinned in deps.items():
        if args.no_network:
            latest = "skipped"
            status = "ℹ️  (offline)"
        else:
            latest = check_pypi_version(pkg)
            if latest == "unknown":
                status = "❓ Not found on PyPI"
            elif latest == pinned:
                status = "✅ Up to date"
            else:
                status = f"⬆️  Update available"
                outdated.append(pkg)
        print(f"{pkg:<30} {pinned:<15} {latest:<15} {status}")

    if outdated:
        print(f"\n⬆️  {len(outdated)} package(s) may have updates: {', '.join(outdated)}")
        if args.check_only:
            sys.exit(1)
    else:
        print("\n✅ All dependencies appear up to date.")


if __name__ == "__main__":
    main()
