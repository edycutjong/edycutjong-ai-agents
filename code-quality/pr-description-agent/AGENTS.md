# PR Description Agent

## Overview
Auto-generates pull request descriptions from git diffs — includes context, change summary, test coverage, and breaking change warnings.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Parse git diff to understand changes
- Generate structured PR description
- Detect breaking changes
- Summarize changes by file/component
- Include test coverage impact
- Add related issue references
- Conventional commit detection
- Screenshot placeholder suggestions
- Reviewer suggestion based on file ownership

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
