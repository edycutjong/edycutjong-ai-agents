# Data Pipeline Validator

## Overview
Validates ETL pipelines, checks data integrity between source and destination systems.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Compare row counts source vs destination
- Validate column types and schemas
- Check for data loss or corruption
- Verify transformation logic
- Generate validation reports
- Support SQL/CSV/Parquet sources
- Schedule recurring validations
- Alert on data quality regressions

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `ui.py` — Ui

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
