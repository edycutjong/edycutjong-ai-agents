# Workout Planner

## Overview
Creates personalized workout plans based on fitness goals, equipment, and schedule.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept fitness goals and level
- Consider available equipment
- Generate weekly workout schedule
- Include warm-up and cool-down
- Calculate estimated calories burned
- Progress difficulty over time
- Support multiple workout types
- Export as formatted PDF/Markdown

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
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
