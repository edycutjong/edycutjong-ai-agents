# Training Data Generator

## Overview
Generates synthetic training data from specifications and seed examples.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept data schema and examples
- Generate diverse synthetic samples
- Maintain statistical distribution
- Support text/tabular/image metadata
- Export in JSONL/CSV/Parquet formats
- Apply data augmentation techniques
- Validate generated data quality
- Scale to configurable dataset sizes

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
