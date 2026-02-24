# Documentation Writer Bot

## Overview
Agent that reads codebases and generates/updates documentation folders.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Scan file structure\n- Read code (functions/classes)\n- Generate Markdown docs\n- Update existing docs (diff aware)\n- Create diagrams (Mermaid)\n- API reference generation\n- Commit changes\n- Tone configuration

## File Structure
- `agent/` — Agent module
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
