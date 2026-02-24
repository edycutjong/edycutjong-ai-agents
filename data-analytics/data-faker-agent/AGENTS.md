# Data Faker Agent

## Overview
Generates realistic fake seed data matching schema definitions for testing.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Read database schema or JSON Schema
- Generate contextually realistic data
- Support locale-specific formats
- Handle relationships and foreign keys
- Generate configurable row counts
- Export as SQL INSERT/CSV/JSON
- Maintain referential integrity
- Support custom field generators

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
