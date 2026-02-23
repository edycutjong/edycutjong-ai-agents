# Meeting Notes Organizer 📝

AI-powered agent that processes meeting transcripts, extracts action items, identifies speakers, and generates follow-up emails.

## Features

- **Transcript Summarization** — AI-generated meeting summaries
- **Action Item Extraction** — Tasks with assignees, priorities, and due dates
- **Speaker Diarization** — Identifies participants and their contributions
- **Follow-up Email Draft** — Ready-to-send recap emails
- **Markdown Export** — Portable report generation
- **Searchable Archive** — JSON-backed meeting history with full-text search
- **Mock Integrations** — Jira issue creation & calendar event stubs

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env → add your OpenAI API key

# 3. Run Streamlit UI
streamlit run main.py

# 4. Or use CLI
python cli.py transcript.txt
python cli.py transcript.txt -o report.md
echo "John: Let's ship v2 by Friday" | python cli.py -
python cli.py --dry-run transcript.txt  # No API key needed
```

## CLI Usage

```
python cli.py [-h] [-o OUTPUT] [--dry-run] [--json] [--api-key KEY] source

positional arguments:
  source            Path to transcript file, or '-' for stdin

optional arguments:
  -o, --output      Save output to markdown file
  --dry-run         Process without AI (template-based, no API key needed)
  --json            Output raw JSON instead of markdown
  --api-key KEY     OpenAI API key (overrides .env)
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All tests use mocks — no API key required.

## Project Structure

```
meeting-notes-organizer/
├── main.py              # Streamlit UI
├── cli.py               # CLI interface
├── config.py            # Settings & env vars
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── style.css            # Streamlit custom theme
├── agent/
│   ├── processor.py     # LangChain transcript processing
│   ├── storage.py       # JSON-based meeting archive
│   └── integrations.py  # Jira, Calendar, Email, Markdown export
├── prompts/
│   └── system_prompts.py  # AI system prompts
└── tests/
    ├── conftest.py        # Shared fixtures
    ├── test_processor.py  # Processor tests (8)
    ├── test_storage.py    # Storage tests (9)
    └── test_integrations.py  # Integration tests (8)
```

## Tech Stack

- **Runtime:** Python 3.11+
- **AI:** OpenAI API via LangChain
- **UI:** Streamlit
- **Storage:** JSON (local file)
- **Testing:** pytest + unittest.mock
