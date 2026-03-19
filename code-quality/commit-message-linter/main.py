"""
Commit Message Linter — validates commit messages against Conventional Commits spec.
Usage: python main.py "feat(auth): add OAuth2 login"
       python main.py --stdin  (reads from stdin, for git hook use)
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Commit Linter] Ready.\n\nPaste one or more commit messages to validate against Conventional Commits spec (feat, fix, docs, refactor, test, chore, etc.)."


TYPES = {"feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"}
PATTERN = re.compile(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?\: (?P<desc>.+)$")
MAX_SUBJECT_LEN = 72


def lint_message(msg: str) -> list:
    issues = []
    subject = msg.splitlines()[0] if msg.splitlines() else msg

    if len(subject) > MAX_SUBJECT_LEN:
        issues.append(f"⚠️  Subject too long ({len(subject)} chars, max {MAX_SUBJECT_LEN})")

    m = PATTERN.match(subject)
    if not m:
        issues.append(f"❌ Does not follow Conventional Commits format: <type>(scope): description")
        issues.append(f"   Example: feat(auth): add OAuth2 login")
        return issues

    commit_type = m.group("type")
    desc = m.group("desc")

    if commit_type not in TYPES:
        issues.append(f"❌ Unknown type '{commit_type}'. Valid: {', '.join(sorted(TYPES))}")

    if desc[0].isupper():
        issues.append(f"⚠️  Description should start lowercase: '{desc}'")

    if desc.endswith("."):
        issues.append(f"⚠️  Description should not end with period.")

    if not issues:
        issues.append(f"✅ Valid commit message.")
        if m.group("breaking"):
            issues.append("🚨 BREAKING CHANGE detected.")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Lint commit messages against Conventional Commits")
    parser.add_argument("message", nargs="?", help="Commit message to lint")
    parser.add_argument("--stdin", action="store_true", help="Read message from stdin (for git hooks)")
    parser.add_argument("--file", default="", help="Read messages from file (one per line)")
    args = parser.parse_args()

    messages = []
    if args.stdin:
        messages = [sys.stdin.read().strip()]  # pragma: no cover
    elif args.file:
        with open(args.file) as f:  # pragma: no cover
            messages = [l.strip() for l in f if l.strip()]  # pragma: no cover
    elif args.message:
        messages = [args.message]
    else:
        print("Commit Message Linter")
        print('Usage: python main.py "feat(auth): add OAuth2 login"')
        print("       python main.py --stdin  # for git hooks")
        sys.exit(0)

    all_ok = True
    for msg in messages:
        print(f"\nMessage: {msg[:80]}")
        issues = lint_message(msg)
        for issue in issues:
            print(f"  {issue}")
        if any("❌" in i for i in issues):
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
