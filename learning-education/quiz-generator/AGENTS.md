# Quiz Generator

## Overview
Reads educational content and generates multiple-choice and open-ended quizzes.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse educational content (text/PDF)
- Generate multiple-choice questions
- Generate open-ended questions
- Create answer keys with explanations
- Adjust difficulty levels
- Tag questions by topic
- Export as Markdown/JSON
- Generate quiz scoring rubrics

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
