import json
import logging
import random
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_jira_issue(title, description, assignee="Unassigned", priority="Medium"):
    """
    Mock function to create a Jira issue.
    Replace with real Jira API integration when ready.
    """
    issue_key = f"PROJ-{random.randint(100, 999)}"
    logger.info(f"Creating Jira issue: {title} assigned to {assignee} ({priority}) -> {issue_key}")
    return {
        "status": "success",
        "key": issue_key,
        "message": f"Created Jira issue {issue_key}",
    }


def create_calendar_event(title, date, description):
    """
    Mock function to create a calendar event.
    Replace with Google Calendar API when ready.
    """
    event_id = f"evt_{random.randint(1000, 9999)}"
    logger.info(f"Creating Calendar event: {title} on {date} -> {event_id}")
    return {
        "status": "success",
        "event_id": event_id,
        "message": f"Scheduled '{title}' for {date}",
    }


def draft_followup_email(summary, action_items):
    """Generate a plain-text follow-up email (no AI, template-based)."""
    lines = [
        "Hi team,",
        "",
        "Thank you for attending today's meeting. Here's a quick recap:",
        "",
        "## Summary",
        summary,
        "",
        "## Action Items",
    ]

    if action_items:
        for item in action_items:
            task = item.get("task", "N/A")
            assignee = item.get("assignee", "Unassigned")
            due = item.get("due_date") or "TBD"
            lines.append(f"- **{task}** → {assignee} (Due: {due})")
    else:
        lines.append("- No action items identified.")

    lines.extend(["", "Best regards,", "Meeting Notes Organizer"])
    return "\n".join(lines)


def export_to_markdown(result, transcript=None):
    """Export processed meeting result to a Markdown string."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Meeting Notes — {now}",
        "",
    ]

    # Summary
    lines.append("## Summary")
    lines.append(result.get("summary", "No summary available."))
    lines.append("")

    # Speakers
    speakers = result.get("speakers", [])
    if speakers:
        lines.append("## Speakers")
        for s in speakers:
            name = s.get("name", "Unknown")
            role = s.get("role", "Unknown")
            pct = s.get("talk_percentage", "?")
            lines.append(f"- **{name}** ({role}) — ~{pct}% of discussion")
        lines.append("")

    # Action Items
    lines.append("## Action Items")
    action_items = result.get("action_items", [])
    if action_items:
        lines.append("| Task | Assignee | Priority | Due |")
        lines.append("|------|----------|----------|-----|")
        for item in action_items:
            task = item.get("task", "N/A")
            assignee = item.get("assignee", "Unassigned")
            priority = item.get("priority", "Medium")
            due = item.get("due_date") or "TBD"
            lines.append(f"| {task} | {assignee} | {priority} | {due} |")
    else:
        lines.append("No action items identified.")
    lines.append("")

    # Email Draft
    email = result.get("email_draft", "")
    if email:
        lines.append("## Follow-up Email Draft")
        lines.append(email)
        lines.append("")

    # Original Transcript
    if transcript:
        lines.append("---")
        lines.append("")
        lines.append("<details><summary>Original Transcript</summary>")
        lines.append("")
        lines.append(transcript)
        lines.append("")
        lines.append("</details>")

    return "\n".join(lines)
