# Monorepo Setup Agent

## Overview
Scaffolds monorepo structures with workspaces, shared packages, and CI pipelines.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Generate Turborepo/Nx workspace
- Create shared package structure
- Configure npm/pnpm workspaces
- Set up shared tsconfig
- Generate CI pipeline configs
- Add changeset configuration
- Create package publishing setup
- Include documentation templates

## File Structure
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
