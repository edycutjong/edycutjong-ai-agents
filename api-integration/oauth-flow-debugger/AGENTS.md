# OAUTH Flow Debugger

## Overview
Traces OAuth 2.0 flows step-by-step, identifies misconfigurations, and suggests fixes.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Trace authorization code flow
- Trace client credentials flow
- Inspect token payloads (JWT decode)
- Validate redirect URI configurations
- Check scope permissions
- Detect common misconfigurations
- Generate flow sequence diagrams
- Test token refresh cycles

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
