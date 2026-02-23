# AGENTS.md — JSON Schema Generator

## Overview
Analyzes JSON data samples and generates comprehensive JSON Schema definitions. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Infer types from JSON samples
- Generate JSON Schema draft-07/2020-12
- Detect optional vs required fields
- Handle nested objects and arrays
- Generate TypeScript interfaces alongside
- Validate sample data against schema
- Support multiple input samples
- Export schema with descriptions

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
