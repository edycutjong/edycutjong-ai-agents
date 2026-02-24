# SLA Monitor

## Overview
Tracks SLA compliance, calculates uptime percentages, and alerts on breaches.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Define SLA targets per service
- Calculate uptime percentages
- Track response time SLAs
- Generate compliance reports
- Alert on SLA breaches
- Historical trend analysis
- Support multiple SLA tiers
- Export reports for stakeholders

## File Structure
- `README.md` — Documentation
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
