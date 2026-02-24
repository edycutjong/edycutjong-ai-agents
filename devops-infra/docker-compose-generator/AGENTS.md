# DOCKER Compose Generator

## Overview
Reads project structure and generates optimized Docker and Docker Compose configurations.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Scan project for language/framework
- Generate multi-stage Dockerfiles
- Create docker-compose.yml with services
- Add health checks and restart policies
- Configure networking and volumes
- Optimize image sizes
- Generate .dockerignore files
- Support dev/staging/prod profiles

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
