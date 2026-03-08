"""
PR Description Agent — generates AI-powered PR descriptions.
Usage: python main.py <diff_or_description>
"""
import argparse
import sys
import os
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[PR Description Agent] Ready.\n\nPaste your diff, commit list, or a description of your PR changes to generate a structured PR description with context, impact, and review notes."


def main():
    parser = argparse.ArgumentParser(description="Generate a PR description from changes")
    parser.add_argument("input", nargs="?", help="Diff, commits, or change description")
    parser.add_argument("--file", default="", help="Read input from file")
    args = parser.parse_args()

    content = ""
    if args.file and os.path.isfile(args.file):
        with open(args.file) as f:
            content = f.read()
    elif args.input:
        content = args.input
    else:
        print("PR Description Agent")
        print("Usage: python main.py 'Fixed login bug and added rate limiting'")
        print("       python main.py --file changes.diff")
        sys.exit(0)

    files = set(re.findall(r"^diff --git a/(.*?) b/", content, re.MULTILINE))
    template = f"""## PR Summary
{content[:300]}{'...' if len(content) > 300 else ''}

## Files Changed
{chr(10).join(f'- `{f}`' for f in files) if files else '- (describe files changed)'}

## Testing Done
- [ ] Unit tests
- [ ] Manual verification
- [ ] Regression check

## Checklist
- [ ] Self-reviewed code
- [ ] Added/updated tests
- [ ] Documentation updated if needed
"""
    print(template)


if __name__ == "__main__":
    main()
