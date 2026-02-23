# AGENTS.md — Gift Recommendation Agent

## Overview
Suggests personalized gift ideas based on recipient profile, occasion, and budget. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept recipient profile details
- Consider occasion and relationship
- Filter by budget range
- Generate ranked gift suggestions
- Include purchase links
- Support multiple categories
- Track past gift history
- Generate gift guide documents

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
