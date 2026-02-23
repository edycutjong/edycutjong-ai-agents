import pytest
from datetime import datetime, timedelta
import pytz
import sys
import os

# Add the project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.scheduler import (
    MeetingScheduler, Participant, MeetingConstraints, TimeSlot
)

# Helper to create timezone-aware datetime
def dt(year, month, day, hour, minute, tz_name="UTC"):
    tz = pytz.timezone(tz_name)
    return tz.localize(datetime(year, month, day, hour, minute))

def test_add_availability_timezone_conversion():
    p = Participant("Alice", "US/Eastern")
    # 9 AM EST is 14:00 UTC (standard time) or 13:00 UTC (daylight saving)
    # Using a fixed date in winter (standard time) -> UTC-5
    start = datetime(2023, 1, 1, 9, 0) # Naive, treated as US/Eastern by method
    end = datetime(2023, 1, 1, 10, 0)

    p.add_availability(start, end)

    assert len(p.availability) == 1
    slot = p.availability[0]
    assert slot.start.tzinfo == pytz.UTC
    assert slot.start.hour == 14 # 9 + 5
    assert slot.end.hour == 15

def test_find_common_slots_simple_overlap():
    scheduler = MeetingScheduler()

    p1 = Participant("Alice", "UTC")
    p1.add_availability(dt(2023, 1, 1, 9, 0), dt(2023, 1, 1, 12, 0))

    p2 = Participant("Bob", "UTC")
    p2.add_availability(dt(2023, 1, 1, 10, 0), dt(2023, 1, 1, 13, 0))

    scheduler.add_participant(p1)
    scheduler.add_participant(p2)

    constraints = MeetingConstraints(duration_minutes=60)
    slots = scheduler.find_common_slots(constraints)

    # Overlap is 10-12.
    # Slots of 60 mins: 10:00-11:00, 10:30-11:30, 11:00-12:00
    assert len(slots) == 3
    assert slots[0].start == dt(2023, 1, 1, 10, 0)
    assert slots[0].end == dt(2023, 1, 1, 11, 0)

def test_find_common_slots_no_overlap():
    scheduler = MeetingScheduler()

    p1 = Participant("Alice", "UTC")
    p1.add_availability(dt(2023, 1, 1, 9, 0), dt(2023, 1, 1, 10, 0))

    p2 = Participant("Bob", "UTC")
    p2.add_availability(dt(2023, 1, 1, 11, 0), dt(2023, 1, 1, 12, 0))

    scheduler.add_participant(p1)
    scheduler.add_participant(p2)

    constraints = MeetingConstraints(duration_minutes=30)
    slots = scheduler.find_common_slots(constraints)

    assert len(slots) == 0

def test_find_common_slots_multiple_participants():
    scheduler = MeetingScheduler()

    p1 = Participant("Alice", "UTC") # 9-12
    p1.add_availability(dt(2023, 1, 1, 9, 0), dt(2023, 1, 1, 12, 0))

    p2 = Participant("Bob", "UTC") # 10-13
    p2.add_availability(dt(2023, 1, 1, 10, 0), dt(2023, 1, 1, 13, 0))

    p3 = Participant("Charlie", "UTC") # 10:30-11:30
    p3.add_availability(dt(2023, 1, 1, 10, 30), dt(2023, 1, 1, 11, 30))

    scheduler.add_participant(p1)
    scheduler.add_participant(p2)
    scheduler.add_participant(p3)

    constraints = MeetingConstraints(duration_minutes=30)
    slots = scheduler.find_common_slots(constraints)

    # Common intersection: 10:30-11:30
    # Slots of 30 mins: 10:30-11:00, 11:00-11:30
    assert len(slots) == 2
    assert slots[0].start == dt(2023, 1, 1, 10, 30)
    assert slots[1].start == dt(2023, 1, 1, 11, 0)

def test_rank_slots_working_hours():
    scheduler = MeetingScheduler()

    # Alice in UTC (Working 9-17)
    p1 = Participant("Alice", "UTC")

    # Bob in UTC+2 (Working 9-17 local -> 7-15 UTC)
    p2 = Participant("Bob", "Etc/GMT-2")

    scheduler.add_participant(p1)
    scheduler.add_participant(p2)

    # Slot 1: 10:00 UTC (Alice: 10, Bob: 12). Both in working hours.
    slot1 = TimeSlot(dt(2023, 1, 1, 10, 0), dt(2023, 1, 1, 11, 0))

    # Slot 2: 16:00 UTC (Alice: 16, Bob: 18). Bob is outside working hours (18 > 17).
    slot2 = TimeSlot(dt(2023, 1, 1, 16, 0), dt(2023, 1, 1, 17, 0))

    constraints = MeetingConstraints(duration_minutes=60, working_hours_start=9, working_hours_end=17)

    ranked = scheduler.rank_slots([slot1, slot2], constraints)

    # slot1 should have higher score
    assert ranked[0][0] == slot1
    assert ranked[0][1] > ranked[1][1]

def test_generate_ics():
    scheduler = MeetingScheduler()
    slot = TimeSlot(dt(2023, 1, 1, 10, 0), dt(2023, 1, 1, 11, 0))
    ics_content = scheduler.generate_ics(slot, "Test Meeting")
    assert "BEGIN:VCALENDAR" in ics_content
    assert "SUMMARY:Test Meeting" in ics_content
