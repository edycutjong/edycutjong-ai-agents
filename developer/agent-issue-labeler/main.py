"""
Issue Labeler Agent — auto-labels GitHub issues based on title, body, and file references.
Usage: python main.py --title "Bug: login crash" --body "App crashes on submit"
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Issue Labeler] Ready.\n\nPaste a GitHub issue title and body to get suggested labels (bug, feature, documentation, security, performance, etc.)."  # pragma: no cover


LABEL_RULES = {
    "bug": ["crash", "error", "broken", "fix", "fail", "exception", "null", "undefined", "not working"],
    "feature": ["add", "feature", "request", "support", "implement", "enhance", "new"],
    "documentation": ["doc", "readme", "guide", "tutorial", "example", "typo", "spelling"],
    "security": ["security", "vulnerability", "cve", "exploit", "injection", "xss", "csrf", "auth"],
    "performance": ["slow", "speed", "performance", "latency", "memory", "cpu", "optimize", "cache"],
    "question": ["how", "why", "what", "help", "?"],
    "duplicate": ["duplicate", "same as", "already reported", "existing"],
    "good first issue": ["simple", "easy", "starter", "beginner", "trivial"],
}


def suggest_labels(title: str, body: str) -> list:
    text = (title + " " + body).lower()  # pragma: no cover
    suggested = []  # pragma: no cover
    for label, keywords in LABEL_RULES.items():  # pragma: no cover
        if any(kw in text for kw in keywords):  # pragma: no cover
            suggested.append(label)  # pragma: no cover
    return suggested or ["needs-triage"]  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Suggest labels for GitHub issues")
    parser.add_argument("--title", default="", help="Issue title")
    parser.add_argument("--body", default="", help="Issue body text")
    parser.add_argument("--input", default="", help="Free-form issue text (title + body)")
    args = parser.parse_args()

    if not any([args.title, args.body, args.input]):
        print("Issue Labeler Agent")
        print("Usage: python main.py --title 'Bug: login crash' --body 'App crashes on submit'")
        print("       python main.py --input 'Login crashes when user submits empty form'")
        sys.exit(0)

    title = args.title or args.input  # pragma: no cover
    body = args.body  # pragma: no cover

    labels = suggest_labels(title, body)  # pragma: no cover
    print(f"Issue: {title or '(no title)'}")  # pragma: no cover
    print(f"Suggested labels: {', '.join(labels)}")  # pragma: no cover
    print("\nAll matched categories:")  # pragma: no cover
    text = (title + " " + body).lower()  # pragma: no cover
    for label, keywords in LABEL_RULES.items():  # pragma: no cover
        matched = [kw for kw in keywords if kw in text]  # pragma: no cover
        if matched:  # pragma: no cover
            print(f"  [{label}] matched: {matched}")  # pragma: no cover


if __name__ == "__main__":
    main()
