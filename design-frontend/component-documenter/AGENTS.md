# AGENTS.md — Component Documenter

## Overview
Reads React/Vue/Svelte components and generates Storybook-style documentation. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse component props/types
- Generate interactive examples
- Document component variants
- Create usage guidelines
- Generate prop tables
- Extract JSDoc/TSDoc comments
- Support React/Vue/Svelte/Angular
- Export as MDX/Markdown

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
