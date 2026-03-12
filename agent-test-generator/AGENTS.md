# Test Generator

## Overview
Reads source code and generates comprehensive unit and integration test suites with high coverage.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Analyze function signatures and types
- Generate unit tests per function
- Generate edge case tests
- Generate integration tests
- Support for Jest and pytest
- Mock dependency generation
- Coverage report integration
- Test description generation

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
