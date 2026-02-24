# Meeting Scheduler Agent

## Overview
Finds optimal meeting times across calendars and time zones using AI.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept participant availability
- Handle multiple time zones
- Find optimal meeting slots
- Respect working hours preferences
- Suggest multiple options ranked
- Generate calendar invites
- Handle recurring meetings
- Integrate with Google/Outlook calendars

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
