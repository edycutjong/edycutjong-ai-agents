# API Changelog Differ

## Overview
Compares API versions (OpenAPI specs), generates detailed migration guides.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Compare two OpenAPI spec versions
- Detect added/removed/changed endpoints
- Identify breaking changes
- Generate migration guide
- Categorize changes by severity
- Create developer changelog
- Support JSON/YAML specs
- Highlight deprecated endpoints

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
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
