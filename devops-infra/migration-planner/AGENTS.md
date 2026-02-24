# Migration Planner

## Overview
Analyzes database schemas and generates migration plans with rollback strategies.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Compare source and target schemas
- Generate step-by-step migration plan
- Create rollback procedures
- Estimate migration duration
- Identify breaking changes
- Generate migration SQL scripts
- Validate data integrity checks
- Support PostgreSQL/MySQL/SQLite

## File Structure
- `__init__.py` — Package init
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `examples/` — Examples module
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
