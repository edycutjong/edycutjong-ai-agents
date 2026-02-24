# HTML To Markdown Converter

## Overview
Scrapes and converts HTML pages to clean, well-formatted Markdown documentation.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse HTML with tag hierarchy
- Convert to clean Markdown
- Preserve headings and lists
- Handle tables and code blocks
- Extract and download images
- Clean up boilerplate/nav/footer
- Support batch URL processing
- Maintain internal link structure

## File Structure
- `agent/` — Agent module
- `app.py` — Application entry
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `test_output/` — Test Output module
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
