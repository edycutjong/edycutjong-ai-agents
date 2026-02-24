# Tweet Thread Writer

## Overview
Converts long-form content into optimized Twitter/X threads with hooks and CTAs.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept long-form content input
- Break into tweet-sized chunks (280 chars)
- Write attention-grabbing opening hook
- Add numbering and flow transitions
- Include relevant hashtags
- Generate call-to-action ending
- Suggest media attachment points
- Preview full thread before export

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
