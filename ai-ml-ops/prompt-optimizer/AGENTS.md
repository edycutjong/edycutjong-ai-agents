# Prompt Optimizer

## Overview
Takes AI prompts, runs A/B variants, measures output quality, and suggests improvements.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept input prompts and test cases
- Generate prompt variations
- Run A/B tests against LLM APIs
- Score outputs for quality/relevance
- Suggest optimized prompts
- Track prompt version history
- Compare across different models
- Export results as report

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
