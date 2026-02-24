# Color Palette Generator

## Overview
Generates harmonious color palettes from images, brand descriptions, or mood keywords.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Generate palettes from text descriptions
- Extract colors from images
- Create complementary/analogous schemes
- Generate CSS custom properties
- Create Tailwind color configs
- Check WCAG contrast ratios
- Export as ASE/JSON/CSS
- Support dark/light mode variants

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
