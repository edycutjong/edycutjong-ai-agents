from pathlib import Path
from typing import List
from .tracker import JournalEntry
import config

EXPORTS_DIR = config.EXPORTS_DIR

def export_to_markdown(entries: List[JournalEntry], filename: str = "journal_export.md") -> Path:
    """Exports a list of journal entries to a Markdown file."""
    filepath = EXPORTS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# My Journal Entries\n\n")

        for entry in sorted(entries, key=lambda x: x.timestamp, reverse=True):
            date_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
            f.write(f"## {date_str}\n\n")

            if entry.mood_entry:
                f.write(f"**Mood:** {entry.mood_entry.mood} | **Energy:** {entry.mood_entry.energy}/10\n")
                if entry.mood_entry.context:
                    f.write(f"**Context:** {entry.mood_entry.context}\n")
                f.write("\n")

            f.write(f"### Prompt\n{entry.prompt}\n\n")
            f.write(f"### Entry\n{entry.response}\n\n")
            f.write("---\n\n")

    return filepath
