import datetime
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass, field
import pytz
from icalendar import Calendar, Event
from dateutil import parser

@dataclass
class TimeSlot:
    start: datetime.datetime
    end: datetime.datetime

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)

    def __str__(self):
        return f"{self.start.isoformat()} to {self.end.isoformat()}"

@dataclass
class Participant:
    name: str
    timezone: str
    availability: List[TimeSlot] = field(default_factory=list)

    def add_availability(self, start: datetime.datetime, end: datetime.datetime):
        # Ensure timestamps are timezone-aware
        tz = pytz.timezone(self.timezone)

        if start.tzinfo is None:
            start = tz.localize(start)
        else:
            start = start.astimezone(tz)

        if end.tzinfo is None:
            end = tz.localize(end)
        else:
            end = end.astimezone(tz)

        # Store as UTC
        self.availability.append(TimeSlot(
            start=start.astimezone(pytz.UTC),
            end=end.astimezone(pytz.UTC)
        ))

@dataclass
class MeetingConstraints:
    duration_minutes: int
    start_date_range: Optional[datetime.datetime] = None
    end_date_range: Optional[datetime.datetime] = None
    working_hours_start: int = 9  # 9 AM
    working_hours_end: int = 17   # 5 PM

class MeetingScheduler:
    def __init__(self):
        self.participants: List[Participant] = []

    def add_participant(self, participant: Participant):
        self.participants.append(participant)

    def find_common_slots(self, constraints: MeetingConstraints) -> List[TimeSlot]:
        if not self.participants:
            return []

        # Start with the availability of the first participant
        common_slots = self.participants[0].availability

        for participant in self.participants[1:]:
            new_common_slots = []
            for slot1 in common_slots:
                for slot2 in participant.availability:
                    intersection = self._get_intersection(slot1, slot2)
                    if intersection and intersection.duration_minutes >= constraints.duration_minutes:
                        new_common_slots.append(intersection)
            common_slots = new_common_slots

        # Filter by constraints (date range) and generate specific slots
        generated_slots = []

        # Ensure constraints dates are UTC aware
        start_limit = constraints.start_date_range
        end_limit = constraints.end_date_range

        if start_limit and start_limit.tzinfo is None:
            start_limit = pytz.UTC.localize(start_limit)
        if end_limit and end_limit.tzinfo is None:
            end_limit = pytz.UTC.localize(end_limit)

        for slot in common_slots:
            slot_start = slot.start
            slot_end = slot.end

            # Apply date range constraints
            if start_limit and slot_end <= start_limit:
                continue
            if end_limit and slot_start >= end_limit:
                continue

            if start_limit and slot_start < start_limit:
                slot_start = start_limit
            if end_limit and slot_end > end_limit:
                slot_end = end_limit

            # If the adjusted slot is still long enough
            if (slot_end - slot_start).total_seconds() / 60 >= constraints.duration_minutes:
                 # Create distinct slots of the meeting duration, stepping by 30 mins
                 current = slot_start
                 while (slot_end - current).total_seconds() / 60 >= constraints.duration_minutes:
                     generated_slots.append(TimeSlot(current, current + datetime.timedelta(minutes=constraints.duration_minutes)))
                     current += datetime.timedelta(minutes=30)

        return generated_slots

    def _get_intersection(self, slot1: TimeSlot, slot2: TimeSlot) -> Optional[TimeSlot]:
        start = max(slot1.start, slot2.start)
        end = min(slot1.end, slot2.end)
        if start < end:
            return TimeSlot(start, end)
        return None

    def rank_slots(self, slots: List[TimeSlot], constraints: MeetingConstraints) -> List[Tuple[TimeSlot, float]]:
        """
        Rank slots based on how many participants are within their working hours.
        Returns a list of (TimeSlot, score). Higher score is better.
        """
        ranked_slots = []
        for slot in slots:
            score = 0
            for participant in self.participants:
                tz = pytz.timezone(participant.timezone)
                local_start = slot.start.astimezone(tz)
                local_end = slot.end.astimezone(tz)

                # Check if entire meeting is within working hours
                # Handle day boundary safely by comparing times only if on same day, otherwise check logic
                # For simplicity, we just check hour range

                s_hour = local_start.hour + local_start.minute / 60.0
                e_hour = local_end.hour + local_end.minute / 60.0

                # Adjust for day overflow if needed (unlikely for 1h meeting but possible)
                if local_start.date() != local_end.date():
                     # Penalize cross-day meetings heavily or just treat as outside working hours
                     pass
                else:
                    if s_hour >= constraints.working_hours_start and e_hour <= constraints.working_hours_end:
                        score += 1
                    elif (s_hour < constraints.working_hours_end and e_hour > constraints.working_hours_start):
                        # Partial overlap
                        score += 0.5

            ranked_slots.append((slot, score))

        # Sort by score descending
        return sorted(ranked_slots, key=lambda x: x[1], reverse=True)

    def generate_ics(self, slot: TimeSlot, subject: str = "Scheduled Meeting", description: str = "") -> str:
        cal = Calendar()
        event = Event()
        event.add('summary', subject)
        event.add('dtstart', slot.start)
        event.add('dtend', slot.end)
        event.add('description', description)
        cal.add_component(event)
        return cal.to_ical().decode("utf-8")
