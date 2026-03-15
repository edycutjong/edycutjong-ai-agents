"""Tests for Meeting Scheduler Agent."""
import pytest
from main import run, suggest_slots, generate_invite


class TestRun:
    def test_run_returns_string(self):
        result = run("")
        assert isinstance(result, str)
        assert "Meeting Scheduler" in result


class TestSuggestSlots:
    def test_returns_5_slots(self):
        slots = suggest_slots(["Alice", "Bob"], 60)
        assert len(slots) == 5

    def test_slots_have_required_keys(self):
        slots = suggest_slots(["Alice"], 30, "UTC")
        for slot in slots:
            assert "start" in slot
            assert "end" in slot
            assert "tz" in slot

    def test_custom_timezone(self):
        slots = suggest_slots(["Alice"], 60, "Asia/Bangkok")
        assert slots[0]["tz"] == "Asia/Bangkok"


class TestGenerateInvite:
    def test_generates_invite_text(self):
        slot = {"start": "Monday, Jan 1 at 9:00 AM", "end": "10:00 AM", "tz": "UTC", "duration": 60}
        invite = generate_invite("Standup", ["Alice", "Bob"], slot)
        assert "Standup" in invite
        assert "Alice" in invite
        assert "Bob" in invite

    def test_includes_notes(self):
        slot = {"start": "Mon", "end": "10AM", "tz": "UTC"}
        invite = generate_invite("Review", ["Alice"], slot, notes="Discuss PR #42")
        assert "PR #42" in invite
