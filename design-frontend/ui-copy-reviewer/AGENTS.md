# AGENTS.md — UI Copy Reviewer

## Overview
Reviews UI text for clarity, consistency, inclusivity, and localizability. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Extract text strings from UI code
- Check for inclusive language
- Verify consistent terminology
- Flag abbreviations and jargon
- Check string localizability
- Suggest clearer alternatives
- Enforce voice and tone guide
- Generate copy review report

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
