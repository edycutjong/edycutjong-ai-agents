# API Rate Limit Tester

## Overview
Stress-tests APIs to map rate limits and generates usage documentation.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Send configurable request bursts
- Detect rate limit headers (X-RateLimit)
- Map rate limit thresholds
- Identify rate limit reset windows
- Generate rate limit documentation
- Test different auth levels
- Visualize rate limit curves
- Suggest client-side throttling

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
