# Documentation Quiz

## Overview
Agent that reads project documentation and generates interactive quizzes to test understanding of APIs, architecture, and best practices.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Parse README/docs into Q&A pairs
- Multiple choice & free-form questions
- Difficulty calibration
- Explanation for correct answers
- Score tracking & progress reports
- Topic-specific quiz generation
- Export as flashcards
- API reference quiz mode

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
