# Infra Cost Analyzer

## Overview
Parses cloud billing data (AWS/GCP/Azure), identifies waste, and suggests right-sizing.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse cloud billing CSVs/APIs
- Identify unused resources
- Suggest instance right-sizing
- Calculate potential savings
- Generate cost reports with charts
- Track spending trends over time
- Alert on budget thresholds
- Compare multi-cloud pricing

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `data/` — Data module
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
