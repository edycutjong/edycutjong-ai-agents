# Model Benchmark Runner

## Overview
Benchmarks LLM models against test suites, comparing cost, quality, and speed.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Define benchmark test suites
- Run tests across multiple LLM providers
- Measure response time and token usage
- Score output quality automatically
- Calculate cost per query
- Generate comparison tables
- Visualize results with charts
- Support OpenAI/Anthropic/Gemini/local models

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
