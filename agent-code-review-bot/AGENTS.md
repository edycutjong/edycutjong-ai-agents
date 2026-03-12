# Code Review Bot

## Overview
Autonomous code review agent that checks style, complexity, security patterns, and suggests improvements.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Analyze code for style issues
- Check cyclomatic complexity
- Detect security anti-patterns
- Suggest performance improvements
- Generate review summary
- Support for Python, JS, TS
- Configurable severity levels
- Inline comment suggestions

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
