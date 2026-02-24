# Log To Metrics Converter

## Overview
Parses unstructured application logs into structured metrics and dashboard configurations.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Parse unstructured log formats
- Extract metrics (latency, error rates, throughput)
- Generate Prometheus metric definitions
- Create Grafana dashboard JSON
- Identify log format patterns
- Map log levels to alert thresholds
- Support multiple log formats
- Generate metric documentation

## File Structure
- `README.md` — Documentation
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
