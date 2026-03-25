# Budget Tracker Agent

## Overview
Personal finance agent that analyzes monthly expenses, categorizes spending patterns, and provides actionable savings recommendations.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- CSV/bank statement import
- Auto expense categorization
- Monthly spending breakdown
- Budget vs actual comparison
- Savings goal tracking
- Spending trend analysis
- Anomaly detection (unusual charges)
- Visual report generation

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
