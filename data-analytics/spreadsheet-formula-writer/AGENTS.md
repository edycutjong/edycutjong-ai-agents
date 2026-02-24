# Spreadsheet Formula Writer

## Overview
Converts natural language questions to Excel/Google Sheets formulas with explanations.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse natural language queries
- Generate Excel formulas (VLOOKUP, INDEX, etc.)
- Generate Google Sheets formulas
- Explain formula logic step-by-step
- Handle complex nested formulas
- Suggest alternatives (XLOOKUP vs VLOOKUP)
- Support array formulas and LAMBDA
- Provide example data demonstrations

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `agent.log` — Agent.Log
- `app.py` — Application entry
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
