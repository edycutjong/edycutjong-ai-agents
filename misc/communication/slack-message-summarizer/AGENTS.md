# Slack Message Summarizer

## Overview
Agent that digests long Slack channels into concise summaries, extracting key decisions, action items, and important mentions.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Channel history ingestion
- Thread-aware summarization
- Action item extraction
- Decision tracking
- Mention & reaction analysis
- Daily/weekly digest generation
- Keyword-based filtering
- Export as markdown report

## File Structure
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## API Keys
- `GEMINI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
