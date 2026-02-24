# Uptime Monitor Agent

## Overview
Polls HTTP endpoints, detects downtime, and sends alerts with diagnostic context.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Poll configurable endpoints at intervals
- Check HTTP status codes and response times
- Detect SSL certificate expiry
- Send alerts via webhook/email
- Generate uptime percentage reports
- Record response time history
- Support custom health check logic
- Dashboard with status page output

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `dashboard.py` — Dashboard
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `uptime.db` — Uptime.Db

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
