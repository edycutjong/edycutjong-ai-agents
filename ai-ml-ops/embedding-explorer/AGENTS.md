# Embedding Explorer

## Overview
Visualizes and searches vector embeddings, finds clusters, outliers, and nearest neighbors.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

## Features
- Load embeddings from files/databases
- Reduce dimensions (t-SNE/UMAP)
- Visualize clusters interactively
- Find nearest neighbors for queries
- Detect outlier embeddings
- Compare embedding models
- Export visualizations
- Support text/image embeddings

## File Structure
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
