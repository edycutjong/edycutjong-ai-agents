# Blog Post Writer

## Overview
Researches topics, creates outlines, and writes SEO-optimized blog posts with sources.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Research topic with web search
- Generate structured outline
- Write SEO-optimized content
- Add meta description and title tags
- Include relevant source citations
- Optimize keyword density
- Generate social media excerpts
- Export as Markdown/HTML

## File Structure
- `agent/` — Agent module
- `app.py` — Application entry
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
