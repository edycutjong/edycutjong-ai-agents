# Changelog Writer

## Overview
Release note agent — Analyze git commit range.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Analyze git commit range
- Group by feat/fix/chore
- Summarize changes
- Generate markdown output
- Publish to release

## File Structure
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `src/` — Src module
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
