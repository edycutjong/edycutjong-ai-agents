# LLM Cost Calculator

## Overview
Tracks token usage across AI providers, forecasts costs, and suggests optimizations.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse API usage logs
- Calculate costs per provider/model
- Forecast monthly spending
- Identify high-cost queries
- Suggest model downgrades for savings
- Compare provider pricing
- Generate cost breakdown reports
- Set budget alerts and thresholds

## File Structure
- `README.md` — Documentation
- `__init__.py` — Package init
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
