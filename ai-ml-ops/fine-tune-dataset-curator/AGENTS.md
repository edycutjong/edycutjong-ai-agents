# Fine Tune Dataset Curator

## Overview
Curates and formats datasets for LLM fine-tuning in JSONL and chat formats.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept raw text/conversation data
- Clean and deduplicate entries
- Format for OpenAI fine-tuning (JSONL)
- Format for Hugging Face datasets
- Validate data quality and consistency
- Balance dataset categories
- Split train/validation sets
- Generate dataset statistics

## File Structure
- `README.md` — Documentation
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
