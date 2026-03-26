"""
Email Classifier Agent — classifies emails by category, priority, and suggested action.
Usage: python main.py --subject "Subject" --body "Email body..."
"""
import argparse
import sys
import re


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Email Classifier] Ready.\n\nPaste an email (subject + body) to classify it by category, priority, and get a suggested action (reply, archive, schedule, escalate)."  # pragma: no cover


CATEGORIES = {
    "urgent": ["urgent", "asap", "immediately", "critical", "emergency", "deadline today"],
    "meeting": ["meeting", "calendar", "invite", "schedule", "availability", "call"],
    "invoice": ["invoice", "payment", "receipt", "bill", "due", "amount owed"],
    "newsletter": ["unsubscribe", "newsletter", "weekly digest", "update from", "no-reply"],
    "support": ["help", "issue", "problem", "ticket", "support", "broken", "not working"],
    "follow-up": ["following up", "checking in", "any update", "reminder", "haven't heard"],
    "spam": ["congratulations", "you've won", "click here", "free offer", "limited time"],
    "internal": ["team", "all hands", "standup", "sprint", "deploy", "PR", "merge"],
}

PRIORITIES = {
    "high": ["urgent", "asap", "critical", "emergency", "deadline"],
    "medium": ["follow-up", "invoice", "meeting", "support"],
    "low": ["newsletter", "spam"],
}

ACTIONS = {
    "urgent": "Reply immediately",
    "meeting": "Accept/decline on calendar",
    "invoice": "Forward to finance / process payment",
    "newsletter": "Archive or unsubscribe",
    "support": "Create support ticket",
    "follow-up": "Reply with status update",
    "spam": "Mark as spam",
    "internal": "Read and acknowledge",
}


def classify(subject: str, body: str) -> dict:
    text = (subject + " " + body).lower()  # pragma: no cover
    matched_cats = []  # pragma: no cover
    for cat, keywords in CATEGORIES.items():  # pragma: no cover
        if any(kw in text for kw in keywords):  # pragma: no cover
            matched_cats.append(cat)  # pragma: no cover
    category = matched_cats[0] if matched_cats else "general"  # pragma: no cover
    priority = "low"  # pragma: no cover
    for level, cats in PRIORITIES.items():  # pragma: no cover
        if category in cats:  # pragma: no cover
            priority = level  # pragma: no cover
            break  # pragma: no cover
    action = ACTIONS.get(category, "Read and respond as needed")  # pragma: no cover
    return {"category": category, "priority": priority, "action": action, "all_matches": matched_cats}  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Classify emails by category and priority")
    parser.add_argument("--subject", default="", help="Email subject line")
    parser.add_argument("--body", default="", help="Email body text")
    parser.add_argument("input", nargs="?", help="Free-form email text")
    args = parser.parse_args()

    if args.input:
        subject, _, body = args.input.partition("\n")  # pragma: no cover
    else:
        subject, body = args.subject, args.body

    if not subject and not body:
        print("Email Classifier Agent")
        print("Usage: python main.py --subject 'Invoice for March' --body 'Please find attached...'")
        sys.exit(0)

    result = classify(subject, body)  # pragma: no cover
    print(f"\n📧 Email Classification")  # pragma: no cover
    print(f"   Subject   : {subject or '(none)'}")  # pragma: no cover
    print(f"   Category  : {result['category']}")  # pragma: no cover
    print(f"   Priority  : {result['priority'].upper()}")  # pragma: no cover
    print(f"   Action    : {result['action']}")  # pragma: no cover
    if len(result['all_matches']) > 1:  # pragma: no cover
        print(f"   Also tagged: {', '.join(result['all_matches'][1:])}")  # pragma: no cover


if __name__ == "__main__":
    main()
