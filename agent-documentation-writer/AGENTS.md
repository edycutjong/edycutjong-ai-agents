# Documentation Writer

## Overview
Reads source code and generates comprehensive README files, API documentation, and inline code comments.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Parse source code structure
- Generate README.md from code
- Generate API reference docs
- Add inline JSDoc/docstring comments
- Detect undocumented functions
- Support for JS, TS, Python
- Configurable documentation style
- Update existing docs incrementally

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
