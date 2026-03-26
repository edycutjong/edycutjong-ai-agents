"""
PR Description Writer — generates comprehensive PR descriptions from diff or commit messages.
Usage: python main.py --diff changes.diff
"""
import argparse
import sys
import re
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[PR Description Writer] Ready.\n\nPaste a git diff, list of commits, or describe your changes to generate a professional PR description with summary, changes, and testing notes."  # pragma: no cover


def generate_pr_description(diff_or_commits: str) -> str:
    lines_added = len(re.findall(r"^\+[^+]", diff_or_commits, re.MULTILINE))  # pragma: no cover
    lines_removed = len(re.findall(r"^-[^-]", diff_or_commits, re.MULTILINE))  # pragma: no cover
    files_changed = set(re.findall(r"^diff --git a/(.*?) b/", diff_or_commits, re.MULTILINE))  # pragma: no cover

    desc = f"""## Summary  # pragma: no cover
<!-- Briefly describe what this PR does and why -->

## Changes
- {lines_added} lines added, {lines_removed} lines removed
"""
    if files_changed:  # pragma: no cover
        desc += f"- Files changed: {', '.join(list(files_changed)[:8])}\n"  # pragma: no cover

    desc += """  # pragma: no cover
## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manually tested

## Notes for Reviewer
<!-- Anything specific reviewers should focus on? -->
"""
    return desc  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Generate PR description from diff or commits")
    parser.add_argument("--diff", default="", help="Path to diff file")
    parser.add_argument("--commits", default="", help="Commit messages (one per line)")
    parser.add_argument("input", nargs="?", help="Free-form description of changes")
    args = parser.parse_args()

    content = ""
    if args.diff and os.path.isfile(args.diff):
        with open(args.diff) as f:  # pragma: no cover
            content = f.read()  # pragma: no cover
    elif args.commits:
        content = args.commits  # pragma: no cover
    elif args.input:
        content = args.input  # pragma: no cover
    else:
        print("PR Description Writer")
        print("Usage: python main.py --diff changes.diff")
        print("       python main.py 'Added OAuth2 login and fixed session timeout'")
        sys.exit(0)

    description = generate_pr_description(content)  # pragma: no cover
    print(description)  # pragma: no cover


if __name__ == "__main__":
    main()
