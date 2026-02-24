# Email Draft Agent

## Overview
Draft professional email replies from bullet points.

## Tech
- Python 3.10+
- Gemini API

## Features
- Bullet point input
- Tone selector
- Length control
- Multiple drafts
- Thread context
- Auto-append email signature
- Copy result to clipboard
- Built-in reusable templates

## File Structure
- `main.py` — Entry point
- `agent/` — Core agent logic
- `config.py` — Configuration & settings
- `requirements.txt` — Dependencies
- `tests/` — Test files
- `.env.example` — Environment variables template

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
