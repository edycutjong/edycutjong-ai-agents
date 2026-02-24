# CRUD API Generator

## Overview
Reads database schemas and generates full CRUD API with validation and documentation.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse database schema (SQL/Prisma)
- Generate REST endpoints (CRUD)
- Add input validation rules
- Generate API documentation
- Include error handling
- Add pagination and filtering
- Generate test files
- Support Express/FastAPI/Flask

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
