# AGENTS.md — Recipe Planner

## Overview
Generates weekly meal plans with recipes based on dietary preferences, allergies, and budget. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept dietary preferences
- Handle food allergies/restrictions
- Generate weekly meal plans
- Create shopping lists
- Calculate nutritional info
- Estimate meal costs
- Suggest meal prep strategies
- Export as formatted Markdown

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
