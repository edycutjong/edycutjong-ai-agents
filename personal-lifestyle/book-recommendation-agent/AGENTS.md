# Book Recommendation Agent

## Overview
Personalized book recommendation agent that suggests reads based on your interests, reading history, and mood preferences.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Interest-based recommendations
- Genre & mood filtering
- Reading list management
- Similar book discovery
- Author exploration
- Reading pace estimation
- Book club discussion questions
- Goodreads-style rating system

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
