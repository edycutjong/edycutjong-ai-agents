# Email Drafter

## Overview
Context-aware response bot — Read incoming email thread.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API
- pytest

## Features
- Read incoming email thread
- Draft polite response
- Check calendar for availability
- Learn user tone
- Save drafts

## File Structure
- `agent_config.py` — Agent configuration
- `config.py` — Configuration & settings
- `email_processor.py` — Email Processor
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
