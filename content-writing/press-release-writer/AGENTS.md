# Press Release Writer

## Overview
Takes product information and generates formatted press releases in standard format.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept product/event details
- Generate AP-style press release
- Include boilerplate sections
- Add relevant quotes
- Format with proper dateline
- Generate for multiple audiences
- Include media contact info
- Export as PDF/Markdown

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
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
