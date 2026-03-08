"""
Issue Labeler Agent — auto-labels GitHub issues based on title, body, and file references.
Usage: python main.py --title "Bug: login crash" --body "App crashes on submit"
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Issue Labeler] Ready.\n\nPaste a GitHub issue title and body to get suggested labels (bug, feature, documentation, security, performance, etc.)."


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
    text = (title + " " + body).lower()
    suggested = []
    for label, keywords in LABEL_RULES.items():
        if any(kw in text for kw in keywords):
            suggested.append(label)
    return suggested or ["needs-triage"]


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

    title = args.title or args.input
    body = args.body

    labels = suggest_labels(title, body)
    print(f"Issue: {title or '(no title)'}")
    print(f"Suggested labels: {', '.join(labels)}")
    print("\nAll matched categories:")
    text = (title + " " + body).lower()
    for label, keywords in LABEL_RULES.items():
        matched = [kw for kw in keywords if kw in text]
        if matched:
            print(f"  [{label}] matched: {matched}")


if __name__ == "__main__":
    main()
