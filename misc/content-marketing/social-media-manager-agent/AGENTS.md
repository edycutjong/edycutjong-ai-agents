# Social Media Manager Agent

## Overview
AI agent to draft, schedule, and engage with social content based on brand voice.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Trend monitoring\n- Draft generation (Text/Image prompts)\n- Platform specific formatting\n- Scheduling/Queue\n- Engagement reply suggestions\n- Analytics summary\n- Brand guideline enforcement\n- Approve/Reject workflow

## File Structure
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
