# Habit Coach

## Overview
Tracks daily habits, analyzes patterns, provides motivational nudges and streak tracking.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Define trackable habits
- Log daily completions
- Calculate streaks and chains
- Analyze completion patterns
- Generate motivational reminders
- Visualize habit heatmaps
- Identify best/worst days
- Generate weekly progress reports

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `analytics.py` — Analytics
- `config.py` — Configuration & settings
- `data/` — Data module
- `main.py` — Entry point
- `models.py` — Models
- `requirements.txt` — Dependencies
- `storage.py` — Storage
- `tests/` — Tests module
- `visualizations.py` — Visualizations

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
