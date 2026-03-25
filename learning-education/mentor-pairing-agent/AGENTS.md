# Mentor Pairing Agent

## Overview
Agent that matches learners with relevant resources, tutorials, and learning paths based on their skill level, goals, and preferred learning style.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Skill assessment questionnaire
- Learning style detection
- Resource recommendation engine
- Personalized learning roadmap
- Progress milestone tracking
- Community resource discovery
- Weakness identification
- Weekly check-in prompts

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
