"""
README Keeper Agent — monitors code changes and keeps README.md in sync.
Usage: python main.py [--check] [--readme README.md] [--source-dir src/]
"""
import argparse
import sys
import os
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[README Keeper] Ready.\n\nPaste your README.md or describe your codebase changes and I'll suggest updates to keep the docs in sync."


def check_readme(readme_path: str, source_dir: str) -> list:
    suggestions = []
    if not os.path.isfile(readme_path):
        return [f"❌ README not found at {readme_path}"]

    with open(readme_path) as f:
        readme = f.read()

    # Check for common sections
    required_sections = ["installation", "usage", "contributing", "license"]
    for section in required_sections:
        if section.lower() not in readme.lower():
            suggestions.append(f"⚠️  Missing section: ## {section.capitalize()}")

    # Check if source dir exists
    if source_dir and os.path.isdir(source_dir):
        py_files = [f for f in os.listdir(source_dir) if f.endswith(".py")]
        if py_files and "python" not in readme.lower():
            suggestions.append("ℹ️  Python files detected but README doesn't mention Python install steps.")

    if not suggestions:
        suggestions.append("✅ README looks up-to-date.")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Check README.md for missing or outdated content")
    parser.add_argument("--readme", default="README.md", help="Path to README.md")
    parser.add_argument("--source-dir", default="src", help="Source directory to validate against")
    parser.add_argument("--check", action="store_true", help="Run check and exit with code 1 if issues found")
    args = parser.parse_args()

    if not os.path.isfile(args.readme) and not args.check:
        print("README Keeper Agent")
        print(f"README not found at '{args.readme}'. Provide a valid path.")
        print("Usage: python main.py --readme README.md --source-dir src/")
        sys.exit(0)

    suggestions = check_readme(args.readme, args.source_dir)
    print(f"\n📖 README Check: {args.readme}")
    for s in suggestions:
        print(f"  {s}")

    if args.check and any("⚠️" in s or "❌" in s for s in suggestions):
        sys.exit(1)


if __name__ == "__main__":
    main()
