from langchain_core.tools import tool
from typing import List, Optional, Dict
from datetime import datetime
from dateutil import parser
import pytz
from .scheduler import MeetingScheduler, Participant, TimeSlot, MeetingConstraints

# Global state for the session
# In a real multi-user app, this would be stored in a database or session context.
scheduler_instance = MeetingScheduler()

@tool
def add_participant(name: str, timezone: str, availability: List[Dict[str, str]]) -> str:
    """
    Adds a participant with their availability.

    Args:
        name: Name of the participant.
        timezone: Timezone string (e.g., "US/Eastern", "UTC").
        availability: List of dicts with 'start' and 'end' keys in ISO format (e.g., "2023-01-01T09:00:00").
                      Example: [{"start": "2023-10-27T10:00:00", "end": "2023-10-27T12:00:00"}]
    """
    try:
        p = Participant(name=name, timezone=timezone)
        for slot in availability:
            start = parser.parse(slot['start'])
            end = parser.parse(slot['end'])
            p.add_availability(start, end)

        scheduler_instance.add_participant(p)
        return f"Added participant {name} with {len(availability)} availability slots."
    except Exception as e:
        return f"Error adding participant: {str(e)}"

@tool
def find_meeting_times(duration_minutes: int, start_date: Optional[str] = None, end_date: Optional[str] = None, working_hours_start: int = 9, working_hours_end: int = 17) -> str:
    """
    Finds common meeting times for all added participants.

    Args:
        duration_minutes: Duration of the meeting in minutes.
        start_date: Optional start date/time constraint (ISO format).
        end_date: Optional end date/time constraint (ISO format).
        working_hours_start: Start of working hours (0-23). Default 9.
        working_hours_end: End of working hours (0-23). Default 17.
    """
    try:
        s_date = parser.parse(start_date) if start_date else None
        e_date = parser.parse(end_date) if end_date else None

        constraints = MeetingConstraints(
            duration_minutes=duration_minutes,
            start_date_range=s_date,
            end_date_range=e_date,
            working_hours_start=working_hours_start,
            working_hours_end=working_hours_end
        )
        slots = scheduler_instance.find_common_slots(constraints)

        if not slots:
            return "No common slots found matching the criteria."

        ranked_slots = scheduler_instance.rank_slots(slots, constraints)

        result = "Found the following potential slots:\n"
        for i, (slot, score) in enumerate(ranked_slots[:5]): # Top 5
            # Format nicely
            result += f"{i+1}. {slot.start.strftime('%Y-%m-%d %H:%M %Z')} to {slot.end.strftime('%H:%M %Z')} (Score: {score})\n"

        return result
    except Exception as e:
        return f"Error finding meeting times: {str(e)}"

@tool
def generate_invite(start_time: str, end_time: str, subject: str = "Scheduled Meeting") -> str:
    """
    Generates an ICS file content for the specified time slot.

    Args:
        start_time: Start time in ISO format.
        end_time: End time in ISO format.
        subject: Meeting subject.
    """
    try:
        start = parser.parse(start_time)
        end = parser.parse(end_time)
        slot = TimeSlot(start, end)

        ics_content = scheduler_instance.generate_ics(slot, subject=subject)

        # Save to file for user convenience (optional, but good for CLI)
        filename = f"invite_{start.strftime('%Y%m%d_%H%M')}.ics"
        with open(filename, "w") as f:
            f.write(ics_content)

        return f"Invite generated and saved to {filename}. Content:\n{ics_content}"
    except Exception as e:
        return f"Error generating invite: {str(e)}"

def get_tools():
    return [add_participant, find_meeting_times, generate_invite]
