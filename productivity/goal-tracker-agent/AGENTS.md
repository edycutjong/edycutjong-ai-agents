# Goal Tracker Agent

## Overview
OKR and goal progress tracking agent that monitors objectives, calculates completion rates, and provides accountability check-ins.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- OKR/SMART goal definition
- Progress percentage tracking
- Key result measurement
- Weekly check-in prompts
- Goal decomposition into tasks
- Completion trend analysis
- At-risk goal detection
- Quarterly review generation

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
