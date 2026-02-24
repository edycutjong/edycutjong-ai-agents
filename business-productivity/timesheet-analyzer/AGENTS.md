# Timesheet Analyzer

## Overview
Analyzes time tracking data, identifies productivity patterns, and suggests improvements.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Import timesheet CSV/API data
- Calculate hours per project/client
- Identify productive time patterns
- Detect overtime trends
- Generate utilization reports
- Compare estimated vs actual hours
- Visualize time distribution
- Suggest scheduling improvements

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
