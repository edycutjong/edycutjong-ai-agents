# Notification Router

## Overview
Smart notification routing agent that analyzes message urgency and routes alerts to the appropriate channel (email, Slack, SMS, push).

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Urgency classification (critical/high/medium/low)
- Multi-channel routing rules
- Quiet hours & DND respect
- Escalation chains
- Deduplication logic
- Template-based message formatting
- Delivery confirmation tracking
- Rule builder CLI

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
