# UI Copy Reviewer

## Overview
Reviews UI text for clarity, consistency, inclusivity, and localizability.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Extract text strings from UI code
- Check for inclusive language
- Verify consistent terminology
- Flag abbreviations and jargon
- Check string localizability
- Suggest clearer alternatives
- Enforce voice and tone guide
- Generate copy review report

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
