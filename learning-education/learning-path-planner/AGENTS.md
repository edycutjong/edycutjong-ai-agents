# Learning Path Planner

## Overview
Analyzes skill gaps and generates personalized learning roadmaps with resources.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept current skill assessment
- Define target skills and roles
- Generate ordered learning path
- Recommend free/paid resources
- Estimate time per milestone
- Track learning progress
- Suggest projects for practice
- Adjust path based on progress

## File Structure
- `__init__.py` — Package init
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
