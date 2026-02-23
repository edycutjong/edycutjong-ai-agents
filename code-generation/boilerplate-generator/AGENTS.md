# AGENTS.md — Boilerplate Generator

## Overview
Generates complete project scaffolds (Next.js, Flask, Express) from feature specifications. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept project specifications
- Generate Next.js/React scaffolds
- Generate Flask/FastAPI scaffolds
- Generate Express/Node scaffolds
- Include authentication boilerplate
- Add database connection setup
- Generate environment config files
- Include Docker and CI configs

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
