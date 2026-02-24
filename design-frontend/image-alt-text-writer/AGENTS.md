# Image Alt Text Writer

## Overview
Scans HTML for images missing alt text and generates descriptive alternatives using AI.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Scan HTML files for img tags
- Detect missing alt attributes
- Generate descriptive alt text with AI
- Handle decorative vs informative images
- Check alt text quality/length
- Generate accessibility report
- Batch process multiple pages
- Support multiple languages

## File Structure
- `README.md` — Documentation
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `reports/` — Reports module
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
