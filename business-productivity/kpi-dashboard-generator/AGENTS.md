# KPI Dashboard Generator

## Overview
Reads data sources and generates KPI dashboards with configurable alerts.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Connect to CSV/API data sources
- Define KPI metrics and targets
- Generate dashboard HTML/JSON
- Create trend visualizations
- Set up threshold-based alerts
- Support real-time data refresh
- Generate executive summary
- Export as PDF/HTML dashboard

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
