# Travel Itinerary Agent

## Overview
Plans detailed travel itineraries with costs, routes, accommodations, and activities.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept destination and travel dates
- Research attractions and activities
- Generate day-by-day itinerary
- Estimate daily costs
- Suggest transportation routes
- Include accommodation options
- Add local dining recommendations
- Export as printable PDF/Markdown

## File Structure
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
