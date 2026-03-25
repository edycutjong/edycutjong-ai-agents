# Pomodoro Coach

## Overview
AI-powered focus session coach that manages Pomodoro intervals, tracks productivity patterns, and provides personalized focus tips.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Configurable work/break intervals
- Session tracking & statistics
- Daily productivity score
- Focus pattern analysis
- Distraction logging
- Streak tracking & motivation
- Task prioritization suggestions
- Weekly productivity report

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
