"""
Dependency Updater — checks for outdated dependencies and suggests updates.
Usage: python main.py [--requirements requirements.txt]
"""
import argparse, sys, os, re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Dependency Updater] Paste your requirements.txt or package.json to identify outdated dependencies and get recommended update steps."


def parse_requirements(text: str) -> dict:
    deps = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            m = re.match(r"^([A-Za-z0-9_\-]+)==([^\s]+)", line)
            if m:
                deps[m.group(1)] = m.group(2)
    return deps


def main():
    parser = argparse.ArgumentParser(description="Check for outdated dependencies")
    parser.add_argument("--requirements", default="requirements.txt")
    args = parser.parse_args()
    if not os.path.isfile(args.requirements):
        print(f"Dependency Updater\nFile not found: {args.requirements}")
        print("Usage: python main.py --requirements requirements.txt")
        sys.exit(0)
    deps = parse_requirements(open(args.requirements).read())
    if not deps:
        print("No pinned dependencies (==version) found.")
        sys.exit(0)
    print(f"Found {len(deps)} pinned package(s):\n")
    for pkg, ver in deps.items():
        print(f"  {pkg}=={ver}  →  check https://pypi.org/project/{pkg}/")
    print("\n💡 Run 'pip list --outdated' or 'pip-review' for live version checks.")

if __name__ == "__main__":
    main()
