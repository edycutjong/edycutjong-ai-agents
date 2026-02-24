# Proposal Writer

## Overview
Generates project proposals from requirements with timeline, budget estimates, and deliverables.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept project requirements input
- Generate executive summary
- Create detailed scope of work
- Estimate timeline with milestones
- Calculate budget breakdown
- List deliverables and acceptance criteria
- Include risk assessment section
- Export as PDF/Markdown

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
