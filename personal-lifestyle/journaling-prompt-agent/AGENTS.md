# Journaling Prompt Agent

## Overview
Generates personalized daily journaling prompts based on mood, goals, and context.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept mood and energy input
- Generate contextual prompts
- Support gratitude journaling
- Include reflection questions
- Track emotional patterns
- Suggest themed prompt sets
- Support multiple journaling styles
- Export journal entries as Markdown

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `data/` — Data module
- `exports/` — Exports module
- `main.py` — Entry point
- `prompts/` — Prompts module
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
