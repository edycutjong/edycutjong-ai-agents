"""
AI PR Reviewer Agent — reviews pull request diffs for code quality, bugs, and improvements.
Usage: python main.py <diff_file_or_text>
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[PR Reviewer] Ready.\n\nPaste a PR diff or describe the changes to get a code review with quality, security, and improvement feedback."


def parse_diff_stats(diff: str) -> dict:
    files_changed = set(re.findall(r"^diff --git a/(.*?) b/", diff, re.MULTILINE))
    additions = len(re.findall(r"^\+[^+]", diff, re.MULTILINE))
    deletions = len(re.findall(r"^-[^-]", diff, re.MULTILINE))
    return {"files": list(files_changed), "additions": additions, "deletions": deletions}


def basic_lint_review(diff: str) -> list:
    issues = []
    if "TODO" in diff or "FIXME" in diff:
        issues.append("⚠️  Found TODO/FIXME comments — resolve before merging.")
    if re.search(r"console\.log|print\(|debugger", diff):
        issues.append("⚠️  Debug statements detected (console.log / print / debugger).")
    if re.search(r"password|secret|api_key|token", diff, re.IGNORECASE):
        issues.append("🔒  Potential secrets or credentials — verify nothing sensitive is hardcoded.")
    if re.search(r"eval\(|exec\(|pickle\.loads", diff):
        issues.append("🚨  Dangerous function detected: eval/exec/pickle.loads — security risk.")
    if not issues:
        issues.append("✅  No obvious issues detected in diff.")
    return issues


def main():
    parser = argparse.ArgumentParser(description="Review a pull request diff")
    parser.add_argument("input", nargs="?", help="Path to diff file or diff text")
    parser.add_argument("--file", help="Read diff from file path")
    args = parser.parse_args()

    diff = ""
    if args.file:
        with open(args.file) as f:
            diff = f.read()
    elif args.input:
        # Could be a file path or raw diff text
        try:
            with open(args.input) as f:
                diff = f.read()
        except (FileNotFoundError, OSError):
            diff = args.input
    else:
        print("AI PR Reviewer Agent")
        print("Usage: python main.py <diff_file>  OR  python main.py --file changes.diff")
        sys.exit(0)

    stats = parse_diff_stats(diff)
    issues = basic_lint_review(diff)

    print("=" * 60)
    print("📋 PR REVIEW REPORT")
    print("=" * 60)
    print(f"Files changed : {len(stats['files'])}")
    print(f"Additions     : +{stats['additions']}")
    print(f"Deletions     : -{stats['deletions']}")
    if stats["files"]:
        print(f"Files         : {', '.join(stats['files'][:5])}")
    print("\n🔍 Issues Found:")
    for issue in issues:
        print(f"  {issue}")
    print("\n💡 Tip: Use the web app for AI-powered detailed review with suggestions.")


if __name__ == "__main__":
    main()
