# LLM Prompt Tester

## Overview
Systematic prompt A/B testing agent that evaluates prompt variations across quality, consistency, and cost metrics to find the optimal prompt.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Prompt variant management
- A/B testing framework
- Quality scoring (relevance, accuracy, coherence)
- Cost-per-response tracking
- Latency benchmarking
- Consistency measurement across runs
- Side-by-side comparison view
- Best prompt recommendation with confidence

## File Structure
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
