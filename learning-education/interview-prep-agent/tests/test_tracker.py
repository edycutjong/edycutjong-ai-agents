import pytest
import os
import json
from agent.tracker import ProgressTracker

def test_save_and_load_session(tmp_path):
    # Use a temporary file for the tracker
    test_file = tmp_path / "test_progress.json"
    tracker = ProgressTracker(filename=str(test_file))

    # Save a session
    tracker.save_session("Coding", "Q1", "A1", 8, "Good")

    # Verify it's in memory
    assert len(tracker.sessions) == 1
    assert tracker.sessions[0].score == 8

    # Verify it's on disk
    assert os.path.exists(test_file)
    with open(test_file, 'r') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]['score'] == 8

    # Load again
    new_tracker = ProgressTracker(filename=str(test_file))
    assert len(new_tracker.sessions) == 1
    assert new_tracker.sessions[0].question == "Q1"

def test_get_stats(tmp_path):
    test_file = tmp_path / "stats_test.json"
    tracker = ProgressTracker(filename=str(test_file))

    tracker.save_session("Coding", "Q1", "A1", 10, "Perfect")
    tracker.save_session("Coding", "Q2", "A2", 5, "Bad")
    tracker.save_session("Behavioral", "Q3", "A3", 9, "Great")

    stats = tracker.get_stats()

    # Overall average: (10 + 5 + 9) / 3 = 8.0
    assert stats["Overall"] == 8.0

    # Coding average: (10 + 5) / 2 = 7.5
    assert stats["Coding"] == 7.5

    # Behavioral average: 9.0
    assert stats["Behavioral"] == 9.0
