# Flashcard Generator

## Overview
Reads technical documentation or notes and generates Anki-compatible flashcards.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse Markdown/PDF/TXT input
- Extract key concepts and terms
- Generate question-answer pairs
- Create cloze deletion cards
- Export in Anki-compatible format
- Tag cards by topic/difficulty
- Generate spaced repetition schedule
- Support multiple subjects

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
