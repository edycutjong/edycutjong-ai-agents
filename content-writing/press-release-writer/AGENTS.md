# AGENTS.md — Press Release Writer

## Overview
Takes product information and generates formatted press releases in standard format. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept product/event details
- Generate AP-style press release
- Include boilerplate sections
- Add relevant quotes
- Format with proper dateline
- Generate for multiple audiences
- Include media contact info
- Export as PDF/Markdown

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
