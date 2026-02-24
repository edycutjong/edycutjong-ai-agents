# FIGMA To CSS Agent

## Overview
Extracts design properties from Figma export files and generates production CSS.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse Figma JSON exports
- Extract layout properties (flex, grid)
- Generate CSS classes
- Convert colors to CSS variables
- Handle responsive breakpoints
- Generate component CSS modules
- Support SCSS/CSS-in-JS output
- Create design system starter

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
