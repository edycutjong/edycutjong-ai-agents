# CI Pipeline Optimizer

## Overview
Analyzes CI/CD configurations, identifies bottlenecks, and suggests parallelization and caching strategies.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse GitHub Actions/GitLab CI configs
- Identify slow pipeline stages
- Suggest parallelization strategies
- Recommend caching improvements
- Estimate time savings
- Generate optimized config files
- Compare before/after metrics
- Support multi-provider configs

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `tests/` — Tests module
- `utils/` — Utils module

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
