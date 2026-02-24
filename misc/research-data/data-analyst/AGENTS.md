# Data Analyst

## Overview
CSV insight generator — Load CSV/Excel data.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API
- pytest

## Features
- Load CSV/Excel data
- Generate summary stats
- Create chart visualizations
- Answer natural language queries
- Export report

## File Structure
- `agent_config.py` — Agent configuration
- `config.py` — Configuration & settings
- `data.csv` — Data.Csv
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
