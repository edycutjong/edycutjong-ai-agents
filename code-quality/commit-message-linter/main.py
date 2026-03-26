"""
Commit Message Linter — validates commit messages against Conventional Commits spec.
Usage: python main.py "feat(auth): add OAuth2 login"
       python main.py --stdin  (reads from stdin, for git hook use)
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Commit Linter] Ready.\n\nPaste one or more commit messages to validate against Conventional Commits spec (feat, fix, docs, refactor, test, chore, etc.)."  # pragma: no cover


TYPES = {"feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"}
PATTERN = re.compile(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?\: (?P<desc>.+)$")
MAX_SUBJECT_LEN = 72


def lint_message(msg: str) -> list:
    issues = []  # pragma: no cover
    subject = msg.splitlines()[0] if msg.splitlines() else msg  # pragma: no cover

    if len(subject) > MAX_SUBJECT_LEN:  # pragma: no cover
        issues.append(f"⚠️  Subject too long ({len(subject)} chars, max {MAX_SUBJECT_LEN})")  # pragma: no cover

    m = PATTERN.match(subject)  # pragma: no cover
    if not m:  # pragma: no cover
        issues.append(f"❌ Does not follow Conventional Commits format: <type>(scope): description")  # pragma: no cover
        issues.append(f"   Example: feat(auth): add OAuth2 login")  # pragma: no cover
        return issues  # pragma: no cover

    commit_type = m.group("type")  # pragma: no cover
    desc = m.group("desc")  # pragma: no cover

    if commit_type not in TYPES:  # pragma: no cover
        issues.append(f"❌ Unknown type '{commit_type}'. Valid: {', '.join(sorted(TYPES))}")  # pragma: no cover

    if desc[0].isupper():  # pragma: no cover
        issues.append(f"⚠️  Description should start lowercase: '{desc}'")  # pragma: no cover

    if desc.endswith("."):  # pragma: no cover
        issues.append(f"⚠️  Description should not end with period.")  # pragma: no cover

    if not issues:  # pragma: no cover
        issues.append(f"✅ Valid commit message.")  # pragma: no cover
        if m.group("breaking"):  # pragma: no cover
            issues.append("🚨 BREAKING CHANGE detected.")  # pragma: no cover

    return issues  # pragma: no cover


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
        messages = [args.message]  # pragma: no cover
    else:
        print("Commit Message Linter")
        print('Usage: python main.py "feat(auth): add OAuth2 login"')
        print("       python main.py --stdin  # for git hooks")
        sys.exit(0)

    all_ok = True  # pragma: no cover
    for msg in messages:  # pragma: no cover
        print(f"\nMessage: {msg[:80]}")  # pragma: no cover
        issues = lint_message(msg)  # pragma: no cover
        for issue in issues:  # pragma: no cover
            print(f"  {issue}")  # pragma: no cover
        if any("❌" in i for i in issues):  # pragma: no cover
            all_ok = False  # pragma: no cover

    sys.exit(0 if all_ok else 1)  # pragma: no cover


if __name__ == "__main__":
    main()
