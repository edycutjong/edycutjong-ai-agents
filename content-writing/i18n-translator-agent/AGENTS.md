# I18N Translator Agent

## Overview
Translate i18n JSON files preserving context.

## Tech
- Python 3.10+
- Gemini API

## Features
- JSON input
- Target language
- Context preservation
- Placeholder safety
- Translate multiple files at once
- Quality review
- Diff preview
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
