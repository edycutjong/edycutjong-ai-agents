# Log Analyzer

## Overview
Ingests application logs, identifies patterns, and surfaces errors with context.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse structured and unstructured logs
- Identify error patterns and frequencies
- Cluster similar log entries
- Timeline visualization of events
- Extract stack traces with context
- Generate summary reports
- Filter by severity/service/time
- Export findings as Markdown

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
