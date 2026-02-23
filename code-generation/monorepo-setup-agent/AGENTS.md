# AGENTS.md — Monorepo Setup Agent

## Overview
Scaffolds monorepo structures with workspaces, shared packages, and CI pipelines. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Generate Turborepo/Nx workspace
- Create shared package structure
- Configure npm/pnpm workspaces
- Set up shared tsconfig
- Generate CI pipeline configs
- Add changeset configuration
- Create package publishing setup
- Include documentation templates

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
