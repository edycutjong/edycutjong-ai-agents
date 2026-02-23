# AGENTS.md — Config File Generator

## Overview
Generates ESLint, Prettier, TSConfig, and other config files from project conventions. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Detect project language and framework
- Generate ESLint configuration
- Generate Prettier configuration
- Generate tsconfig.json
- Generate .editorconfig
- Generate husky/lint-staged configs
- Support monorepo configs
- Apply opinionated best practices

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
