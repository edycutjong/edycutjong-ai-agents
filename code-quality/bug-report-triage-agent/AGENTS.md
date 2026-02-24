# Bug Report Triage Agent

## Overview
Auto-triage bug reports by severity.

## Tech
- Python 3.10+
- Gemini API

## Features
- Bug report input
- Severity classification
- Component detection
- Duplicate check
- Priority scoring
- Assignee suggest
- Auto-assign labels and tags
- Triage report

## File Structure
- `main.py` — Entry point
- `config.py` — Configuration & settings
- `src/agent.py` — Core Gemini agent logic
- `src/utils.py` — Rich console utilities
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
