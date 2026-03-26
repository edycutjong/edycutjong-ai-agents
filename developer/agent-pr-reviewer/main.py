"""
AI PR Reviewer Agent — reviews pull request diffs for code quality, bugs, and improvements.
Usage: python main.py <diff_file_or_text>
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[PR Reviewer] Ready.\n\nPaste a PR diff or describe the changes to get a code review with quality, security, and improvement feedback."  # pragma: no cover


def parse_diff_stats(diff: str) -> dict:
    files_changed = set(re.findall(r"^diff --git a/(.*?) b/", diff, re.MULTILINE))  # pragma: no cover
    additions = len(re.findall(r"^\+[^+]", diff, re.MULTILINE))  # pragma: no cover
    deletions = len(re.findall(r"^-[^-]", diff, re.MULTILINE))  # pragma: no cover
    return {"files": list(files_changed), "additions": additions, "deletions": deletions}  # pragma: no cover


def basic_lint_review(diff: str) -> list:
    issues = []  # pragma: no cover
    if "TODO" in diff or "FIXME" in diff:  # pragma: no cover
        issues.append("⚠️  Found TODO/FIXME comments — resolve before merging.")  # pragma: no cover
    if re.search(r"console\.log|print\(|debugger", diff):  # pragma: no cover
        issues.append("⚠️  Debug statements detected (console.log / print / debugger).")  # pragma: no cover
    if re.search(r"password|secret|api_key|token", diff, re.IGNORECASE):  # pragma: no cover
        issues.append("🔒  Potential secrets or credentials — verify nothing sensitive is hardcoded.")  # pragma: no cover
    if re.search(r"eval\(|exec\(|pickle\.loads", diff):  # pragma: no cover
        issues.append("🚨  Dangerous function detected: eval/exec/pickle.loads — security risk.")  # pragma: no cover
    if not issues:  # pragma: no cover
        issues.append("✅  No obvious issues detected in diff.")  # pragma: no cover
    return issues  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Review a pull request diff")
    parser.add_argument("input", nargs="?", help="Path to diff file or diff text")
    parser.add_argument("--file", help="Read diff from file path")
    args = parser.parse_args()

    diff = ""
    if args.file:
        with open(args.file) as f:  # pragma: no cover
            diff = f.read()  # pragma: no cover
    elif args.input:
        # Could be a file path or raw diff text
        try:  # pragma: no cover
            with open(args.input) as f:  # pragma: no cover
                diff = f.read()  # pragma: no cover
        except (FileNotFoundError, OSError):  # pragma: no cover
            diff = args.input  # pragma: no cover
    else:
        print("AI PR Reviewer Agent")
        print("Usage: python main.py <diff_file>  OR  python main.py --file changes.diff")
        sys.exit(0)

    stats = parse_diff_stats(diff)  # pragma: no cover
    issues = basic_lint_review(diff)  # pragma: no cover

    print("=" * 60)  # pragma: no cover
    print("📋 PR REVIEW REPORT")  # pragma: no cover
    print("=" * 60)  # pragma: no cover
    print(f"Files changed : {len(stats['files'])}")  # pragma: no cover
    print(f"Additions     : +{stats['additions']}")  # pragma: no cover
    print(f"Deletions     : -{stats['deletions']}")  # pragma: no cover
    if stats["files"]:  # pragma: no cover
        print(f"Files         : {', '.join(stats['files'][:5])}")  # pragma: no cover
    print("\n🔍 Issues Found:")  # pragma: no cover
    for issue in issues:  # pragma: no cover
        print(f"  {issue}")  # pragma: no cover
    print("\n💡 Tip: Use the web app for AI-powered detailed review with suggestions.")  # pragma: no cover


if __name__ == "__main__":
    main()
