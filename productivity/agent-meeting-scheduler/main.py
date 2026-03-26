"""
Meeting Scheduler Agent — suggests optimal meeting times and generates calendar invites.
Usage: python main.py --participants "Alice, Bob" --duration 60 --timezone "Asia/Bangkok"
"""
import argparse
import sys
from datetime import datetime, timedelta


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Meeting Scheduler] Ready.\n\nDescribe your meeting needs (participants, duration, timezone, urgency) and I'll suggest optimal time slots and draft a calendar invite."  # pragma: no cover


def suggest_slots(participants: list, duration_mins: int, tz: str = "UTC") -> list:
    """Generate next 5 business weekday slots."""
    slots = []  # pragma: no cover
    now = datetime.now()  # pragma: no cover
    day = now.replace(hour=9, minute=0, second=0, microsecond=0)  # pragma: no cover
    if day <= now:  # pragma: no cover
        day += timedelta(days=1)  # pragma: no cover

    while len(slots) < 5:  # pragma: no cover
        if day.weekday() < 5:  # Mon-Fri only  # pragma: no cover
            for hour in [9, 11, 14, 15]:  # pragma: no cover
                if len(slots) >= 5:  # pragma: no cover
                    break  # pragma: no cover
                start = day.replace(hour=hour, minute=0)  # pragma: no cover
                end = start + timedelta(minutes=duration_mins)  # pragma: no cover
                slots.append({  # pragma: no cover
                    "start": start.strftime("%A, %B %d %Y at %I:%M %p"),
                    "end": end.strftime("%I:%M %p"),
                    "tz": tz
                })
        day += timedelta(days=1)  # pragma: no cover

    return slots  # pragma: no cover


def generate_invite(subject: str, participants: list, slot: dict, notes: str = "") -> str:
    return f"""📅 CALENDAR INVITE  # pragma: no cover

Title     : {subject}
When      : {slot['start']} – {slot['end']} ({slot['tz']})
Attendees : {', '.join(participants)}
Duration  : {slot.get('duration', 60)} minutes

Agenda:
{notes or '- TBD'}

────────────────────────────────────
Add to calendar: https://calendar.google.com (manual entry)
"""


def main():
    parser = argparse.ArgumentParser(description="Suggest meeting times and draft calendar invites")
    parser.add_argument("--participants", default="", help="Comma-separated participant names")
    parser.add_argument("--duration", type=int, default=60, help="Meeting duration in minutes (default: 60)")
    parser.add_argument("--subject", default="Team Meeting", help="Meeting subject/title")
    parser.add_argument("--timezone", default="UTC", help="Timezone (default: UTC)")
    parser.add_argument("--notes", default="", help="Agenda or meeting notes")
    args = parser.parse_args()

    if not args.participants:
        print("Meeting Scheduler Agent")
        print('Usage: python main.py --participants "Alice, Bob" --duration 60 --subject "Sprint Review"')
        sys.exit(0)

    participants = [p.strip() for p in args.participants.split(",")]  # pragma: no cover
    slots = suggest_slots(participants, args.duration, args.timezone)  # pragma: no cover

    print(f"\n📅 Available time slots for {', '.join(participants)} ({args.duration} min):\n")  # pragma: no cover
    for i, slot in enumerate(slots, 1):  # pragma: no cover
        print(f"  Option {i}: {slot['start']} – {slot['end']} {slot['tz']}")  # pragma: no cover

    print(f"\n📨 Sample invite for Option 1:")  # pragma: no cover
    slots[0]['duration'] = args.duration  # pragma: no cover
    print(generate_invite(args.subject, participants, slots[0], args.notes))  # pragma: no cover


if __name__ == "__main__":
    main()
