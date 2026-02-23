# AGENTS.md — Journaling Prompt Agent

## Overview
Generates personalized daily journaling prompts based on mood, goals, and context. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept mood and energy input
- Generate contextual prompts
- Support gratitude journaling
- Include reflection questions
- Track emotional patterns
- Suggest themed prompt sets
- Support multiple journaling styles
- Export journal entries as Markdown

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
