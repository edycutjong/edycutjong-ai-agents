# Chart Generator Agent

## Overview
Takes data and natural language queries, generates chart code (Chart.js, D3, Matplotlib).

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Accept CSV/JSON data input
- Parse natural language chart requests
- Generate Chart.js configurations
- Generate D3.js visualizations
- Generate Matplotlib/Seaborn plots
- Auto-select appropriate chart type
- Customize colors, labels, axes
- Export as HTML/PNG/SVG

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
