# Dead Code Hunter

## Overview
Analyze codebase for unused exports, unreachable code paths, orphan files, and dead CSS selectors across JavaScript/TypeScript projects.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Detect unused exports in JS/TS
- Find orphan files (not imported anywhere)
- Identify unreachable code paths
- Dead CSS selector detection
- Unused dependency detection
- Report with confidence scores
- Suggested safe deletions
- JSON and Markdown output
- Git-aware (ignore recently added files)

## File Structure
- `agent/`
- `config.py`
- `main.py`
- `prompts/`
- `requirements.txt`
- `tests/`

## API Keys
- `GEMINI_API_KEY` — Required

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
