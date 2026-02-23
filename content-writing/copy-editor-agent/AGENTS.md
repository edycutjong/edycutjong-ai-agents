# AGENTS.md — Copy Editor Agent

## Overview
Proofreads text for grammar, style, tone consistency, and readability score. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Check grammar and spelling
- Enforce style guide rules (AP/Chicago)
- Analyze reading level (Flesch-Kincaid)
- Detect passive voice overuse
- Suggest concise alternatives
- Check tone consistency
- Flag jargon and acronyms
- Generate editing summary report

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
