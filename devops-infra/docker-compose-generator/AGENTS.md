# AGENTS.md — Docker Compose Generator

## Overview
Reads project structure and generates optimized Docker and Docker Compose configurations. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan project for language/framework
- Generate multi-stage Dockerfiles
- Create docker-compose.yml with services
- Add health checks and restart policies
- Configure networking and volumes
- Optimize image sizes
- Generate .dockerignore files
- Support dev/staging/prod profiles

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
