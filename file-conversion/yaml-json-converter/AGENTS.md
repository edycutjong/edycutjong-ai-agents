# AGENTS.md — YAML JSON Converter

## Overview
Bi-directional YAML-to-JSON conversion with validation, comments preservation, and formatting. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Convert YAML to JSON
- Convert JSON to YAML
- Preserve YAML comments where possible
- Validate against schemas
- Format with configurable indentation
- Handle multi-document YAML
- Support anchors and aliases
- Batch convert directory of files

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
