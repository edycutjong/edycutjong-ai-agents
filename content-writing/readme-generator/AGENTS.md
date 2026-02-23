# AGENTS.md — README Generator

## Overview
Scans project files and generates comprehensive READMEs with badges, setup guides, and usage examples. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan project structure and tech stack
- Generate installation instructions
- Create usage examples with code
- Add shields.io badges
- Include contributing guidelines
- Generate table of contents
- Detect license and add section
- Support monorepo structures

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
