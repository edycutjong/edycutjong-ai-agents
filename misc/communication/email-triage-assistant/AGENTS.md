# Email Triage Assistant

## Overview
Local AI agent to categorize, summarize, and draft replies to emails.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Connect IMAP/API\n- Categorize (Urgent, Newsletter, Spam)\n- Summarize threads\n- Draft replies style-matched\n- Local LLM support\n- Privacy focus\n- Daily briefing generation\n- Action item extraction

## File Structure
- `__init__.py` — Package init
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
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
