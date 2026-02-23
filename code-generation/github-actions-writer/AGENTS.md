# AGENTS.md — GitHub Actions Writer

## Overview
Reads project structure and generates optimized GitHub Actions CI/CD workflows. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Detect project language and tools
- Generate CI workflow (lint/test/build)
- Generate CD workflow (deploy)
- Add caching for dependencies
- Configure matrix testing
- Set up release automation
- Add security scanning steps
- Generate reusable workflow files

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
