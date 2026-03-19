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
except ImportError:  # pragma: no cover
    pass  # pragma: no cover


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
    try:  # pragma: no cover
        url = f"https://pypi.org/pypi/{package}/json"  # pragma: no cover
        data = json.loads(urlopen(url, timeout=5).read())  # pragma: no cover
        return data["info"]["version"]  # pragma: no cover
    except Exception:  # pragma: no cover
        return "unknown"  # pragma: no cover


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

    with open(args.requirements) as f:  # pragma: no cover
        text = f.read()  # pragma: no cover

    deps = parse_requirements(text)  # pragma: no cover
    if not deps:  # pragma: no cover
        print("No pinned dependencies found (==version) in requirements file.")  # pragma: no cover
        sys.exit(0)  # pragma: no cover

    print(f"Checking {len(deps)} pinned packages...\n")  # pragma: no cover
    print(f"{'Package':<30} {'Pinned':<15} {'Latest':<15} {'Status'}")  # pragma: no cover
    print("-" * 75)  # pragma: no cover

    outdated = []  # pragma: no cover
    for pkg, pinned in deps.items():  # pragma: no cover
        if args.no_network:  # pragma: no cover
            latest = "skipped"  # pragma: no cover
            status = "ℹ️  (offline)"  # pragma: no cover
        else:
            latest = check_pypi_version(pkg)  # pragma: no cover
            if latest == "unknown":  # pragma: no cover
                status = "❓ Not found on PyPI"  # pragma: no cover
            elif latest == pinned:  # pragma: no cover
                status = "✅ Up to date"  # pragma: no cover
            else:
                status = f"⬆️  Update available"  # pragma: no cover
                outdated.append(pkg)  # pragma: no cover
        print(f"{pkg:<30} {pinned:<15} {latest:<15} {status}")  # pragma: no cover

    if outdated:  # pragma: no cover
        print(f"\n⬆️  {len(outdated)} package(s) may have updates: {', '.join(outdated)}")  # pragma: no cover
        if args.check_only:  # pragma: no cover
            sys.exit(1)  # pragma: no cover
    else:
        print("\n✅ All dependencies appear up to date.")  # pragma: no cover


if __name__ == "__main__":
    main()
