from typing import List

def notify_consumers(summary: str, recipients: List[str] = None):
    """
    Simulates sending a notification to consumers about API changes.
    """
    if recipients is None:
        recipients = ["dev-team", "api-consumers"]

    # In a real app, integrate with Slack/Email API here.
    # We use print here as a mock.
    print(f"\n[Notification Tool] Notifying {', '.join(recipients)} about changes...")
    print(f"Summary: {summary}\n")
    return True
