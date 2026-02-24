# Meeting Summarizer

## Overview
Transcript processor — Read VTT/Text transcript.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API
- pytest

## Features
- Read VTT/Text transcript
- Extract action items
- Summarize key decisions
- Draft follow-up email
- Sentiment analysis

## File Structure
- `agent_config.py` — Agent configuration
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `utils.py` — Utils

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
