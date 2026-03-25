# Meditation Guide

## Overview
AI agent that generates personalized guided meditation scripts based on mood, duration, and focus area (stress, sleep, focus, gratitude).

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Mood-based session selection
- Configurable duration (5-30 min)
- Focus areas (stress, sleep, focus, gratitude)
- Progressive relaxation scripts
- Breathing exercise generator
- Daily affirmation creation
- Session history tracking
- Export as text/audio script

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
