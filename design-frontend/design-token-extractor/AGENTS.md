# AGENTS.md — Design Token Extractor

## Overview
Reads Figma files or design specs and generates CSS/SCSS design token variables. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Figma/Sketch design files
- Extract colors, fonts, spacing
- Generate CSS custom properties
- Generate SCSS variables
- Generate Tailwind theme config
- Create consistent naming conventions
- Support light/dark themes
- Export as JSON token format

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
