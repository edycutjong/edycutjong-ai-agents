# Meal Prep Planner

## Overview
Weekly meal prep planning agent that generates recipes, creates grocery lists, and optimizes for nutritional goals and dietary preferences.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Weekly meal plan generation
- Dietary preference support (vegan, keto, etc.)
- Grocery list compilation
- Nutritional breakdown per meal
- Prep time optimization
- Leftover reuse suggestions
- Budget-conscious options
- Recipe export as PDF

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
