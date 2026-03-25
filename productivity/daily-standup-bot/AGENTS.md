# Daily Standup Bot

## Overview
Async daily standup collection agent that gathers team updates, identifies blockers, and generates formatted standup summaries.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Async standup collection via CLI
- Yesterday/Today/Blockers format
- Team summary generation
- Blocker escalation detection
- Trend analysis (recurring blockers)
- Attendance tracking
- Historical standup archive
- Export as Slack/email digest

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
