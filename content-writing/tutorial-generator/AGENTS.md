# AGENTS.md — Tutorial Generator

## Overview
Reads code libraries and generates step-by-step tutorials with runnable examples. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Analyze library API surface
- Generate beginner-friendly tutorials
- Create step-by-step instructions
- Include runnable code examples
- Add prerequisite checklist
- Generate troubleshooting section
- Support multiple difficulty levels
- Export as Markdown with code blocks

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
