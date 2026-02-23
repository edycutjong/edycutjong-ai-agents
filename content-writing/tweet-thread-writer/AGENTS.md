# AGENTS.md — Tweet Thread Writer

## Overview
Converts long-form content into optimized Twitter/X threads with hooks and CTAs. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept long-form content input
- Break into tweet-sized chunks (280 chars)
- Write attention-grabbing opening hook
- Add numbering and flow transitions
- Include relevant hashtags
- Generate call-to-action ending
- Suggest media attachment points
- Preview full thread before export

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
