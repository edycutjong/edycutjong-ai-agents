# CSV Cleaner

## Overview
Ingests messy CSV files, detects and fixes encoding issues, duplicates, missing values, and type mismatches.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Detect and fix file encoding issues
- Remove duplicate rows (exact and fuzzy)
- Handle missing values (fill/drop/interpolate)
- Standardize date and number formats
- Fix column type mismatches
- Remove trailing whitespace and newlines
- Generate data quality report
- Export cleaned CSV with changelog

## File Structure
- `README.md` — Documentation
- `__init__.py` — Package init
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
