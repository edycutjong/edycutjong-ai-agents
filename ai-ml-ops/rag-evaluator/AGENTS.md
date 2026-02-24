# RAG Evaluator

## Overview
Tests RAG pipeline quality by measuring retrieval accuracy and answer relevance.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Define evaluation test cases
- Measure retrieval precision/recall
- Score answer faithfulness
- Detect hallucinations vs source
- Compare different RAG configurations
- Generate evaluation reports
- Support multiple vector stores
- Benchmark latency and cost

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
