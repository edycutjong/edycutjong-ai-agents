# Time Audit Agent

## Overview
Calendar and time usage analysis agent that audits how time is spent and recommends optimizations for better productivity.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Calendar/ICS file import
- Meeting time analysis
- Focus time calculation
- Category breakdown (admin, coding, meetings)
- Meeting overload detection
- Fragmentation score
- Optimization recommendations
- Weekly time audit report

## File Structure
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
