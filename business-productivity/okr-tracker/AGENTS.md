# OKR Tracker

## Overview
Manages Objectives and Key Results, tracks progress, and generates status reports.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Define objectives and key results
- Track progress percentages
- Generate weekly status reports
- Calculate team OKR scores
- Alert on at-risk objectives
- Visualize progress over time
- Support quarterly cycles
- Export reports as Markdown

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
