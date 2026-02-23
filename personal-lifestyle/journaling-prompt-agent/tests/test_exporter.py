import pytest
from pathlib import Path
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agent.exporter import export_to_markdown
from agent.tracker import JournalEntry, MoodEntry
import agent.exporter # to patch EXPORTS_DIR

def test_export_to_markdown(tmp_path, monkeypatch):
    # Patch EXPORTS_DIR in the exporter module
    monkeypatch.setattr(agent.exporter, "EXPORTS_DIR", tmp_path)

    entries = [
        JournalEntry(
            id="1",
            timestamp=datetime(2023, 10, 27, 10, 0),
            prompt="Prompt 1",
            response="Response 1",
            mood_entry=MoodEntry(mood="Happy", energy=9)
        ),
        JournalEntry(
            id="2",
            timestamp=datetime(2023, 10, 28, 11, 0),
            prompt="Prompt 2",
            response="Response 2"
        )
    ]

    filepath = export_to_markdown(entries, "test_export.md")

    assert filepath.exists()
    content = filepath.read_text(encoding="utf-8")

    assert "# My Journal Entries" in content
    assert "2023-10-27 10:00" in content
    assert "**Mood:** Happy" in content
    assert "Prompt 1" in content
    assert "Response 1" in content
    assert "2023-10-28 11:00" in content
