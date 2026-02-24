# Dockerfile Optimizer

## Overview
Analyzes existing Dockerfiles, reduces image size, and improves layer caching.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse existing Dockerfile
- Identify large image layers
- Suggest multi-stage builds
- Optimize COPY instruction ordering
- Recommend smaller base images
- Add proper .dockerignore
- Reduce final image size
- Benchmark before/after sizes

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
