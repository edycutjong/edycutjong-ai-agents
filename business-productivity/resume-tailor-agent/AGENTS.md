# Resume Tailor Agent

## Overview
Tailor resume to match job descriptions.

## Tech
- Python 3.10+
- Gemini API

## Features
- Resume upload
- JD input
- Keyword matching
- Skills alignment
- Experience rewrite
- ATS optimization
- Calculate and display quality score
- Export results in multiple formats

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
