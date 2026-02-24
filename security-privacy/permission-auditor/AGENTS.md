# Permission Auditor

## Overview
Scans app manifests and configurations for excessive permissions and suggests removals.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse Android/iOS manifests
- Analyze Chrome extension permissions
- Compare declared vs used permissions
- Flag unnecessary permissions
- Suggest minimal permission set
- Generate permission justification docs
- Check OAuth scope minimality
- Support web app permission policies

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
