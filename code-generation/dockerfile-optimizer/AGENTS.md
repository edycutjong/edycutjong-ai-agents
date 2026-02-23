# AGENTS.md — Dockerfile Optimizer

## Overview
Analyzes existing Dockerfiles, reduces image size, and improves layer caching. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse existing Dockerfile
- Identify large image layers
- Suggest multi-stage builds
- Optimize COPY instruction ordering
- Recommend smaller base images
- Add proper .dockerignore
- Reduce final image size
- Benchmark before/after sizes

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
