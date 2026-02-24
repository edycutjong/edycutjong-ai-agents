# GRAPHQL Schema Analyzer

## Overview
Analyzes GraphQL schemas, suggests optimizations, and detects N+1 query problems.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse GraphQL SDL schemas
- Detect N+1 query patterns
- Identify unused types and fields
- Suggest query complexity limits
- Analyze resolver patterns
- Generate schema documentation
- Recommend pagination strategies
- Flag circular type references

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
