# Recipe Planner

## Overview
Generates weekly meal plans with recipes based on dietary preferences, allergies, and budget.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept dietary preferences
- Handle food allergies/restrictions
- Generate weekly meal plans
- Create shopping lists
- Calculate nutritional info
- Estimate meal costs
- Suggest meal prep strategies
- Export as formatted Markdown

## File Structure
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
