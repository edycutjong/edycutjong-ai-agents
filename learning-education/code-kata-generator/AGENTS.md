# Code Kata Generator

## Overview
Programming practice problem generator with auto-grading, supporting multiple languages and difficulty levels from beginner to expert.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Multi-language support (Python, JS, Go, Rust)
- Difficulty tiers (beginner/intermediate/expert)
- Auto-generated test cases
- Solution validation & grading
- Hint system with progressive reveals
- Time complexity analysis
- Topic-based filtering (arrays, trees, graphs)
- Progress tracking

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
