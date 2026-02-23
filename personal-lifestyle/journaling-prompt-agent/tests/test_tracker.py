import json
import pytest
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from agent.tracker import Tracker, MoodEntry, JournalEntry

@pytest.fixture
def temp_tracker(tmp_path):
    # Mock config paths by monkeypatching (or just subclassing/overriding if possible)
    # Since Tracker uses global variables from config, we need to patch them or the Tracker class.
    # But Tracker initializes paths in __init__ using config constants.
    # Wait, Tracker.__init__ uses:
    # self.mood_file = MOOD_TRACKER_FILE
    # self.journal_file = JOURNAL_FILE

    # We can overwrite these attributes after initialization.
    tracker = Tracker()
    tracker.mood_file = tmp_path / "mood_tracker.json"
    tracker.journal_file = tmp_path / "journal_entries.json"
    tracker._ensure_files() # Re-run ensure files for temp paths
    return tracker

def test_add_mood(temp_tracker):
    entry = temp_tracker.add_mood("Happy", 8, "Great day")
    assert entry.mood == "Happy"
    assert entry.energy == 8
    assert entry.context == "Great day"

    history = temp_tracker.get_mood_history()
    assert len(history) == 1
    assert history[0].mood == "Happy"

def test_save_journal_entry(temp_tracker):
    mood = MoodEntry(mood="Calm", energy=5)
    entry = JournalEntry(
        id="123",
        prompt="Why?",
        response="Because.",
        mood_entry=mood
    )

    temp_tracker.save_journal_entry(entry)

    saved_entries = temp_tracker.get_journal_entries()
    assert len(saved_entries) == 1
    assert saved_entries[0].id == "123"
    assert saved_entries[0].mood_entry.mood == "Calm"

def test_persistence(temp_tracker):
    temp_tracker.add_mood("Sad", 2)

    # Create a new tracker instance pointing to same files
    new_tracker = Tracker()
    new_tracker.mood_file = temp_tracker.mood_file
    new_tracker.journal_file = temp_tracker.journal_file

    history = new_tracker.get_mood_history()
    assert len(history) == 1
    assert history[0].mood == "Sad"
