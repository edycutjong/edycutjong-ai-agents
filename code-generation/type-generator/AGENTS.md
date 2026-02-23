# AGENTS.md — Type Generator

## Overview
Infers TypeScript and Python type definitions from JSON responses and API data. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept JSON sample data
- Infer TypeScript interfaces
- Infer Python dataclass/Pydantic models
- Handle nested and optional types
- Detect union types
- Generate from API responses
- Support array and enum types
- Export as importable modules

## File Structure
- `main.py`: Entry loop
- `agent/`: Core tool definitions
- `prompts/`: System prompts
- `config.py`: Settings
- `requirements.txt`: Dependencies
- `tests/`: Test files

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
