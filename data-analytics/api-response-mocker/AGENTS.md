# AGENTS.md — API Response Mocker

## Overview
Reads API specs (OpenAPI/Swagger) and generates mock servers with realistic test data. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse OpenAPI/Swagger specifications
- Generate mock HTTP server
- Return realistic sample responses
- Support dynamic path parameters
- Simulate error responses (4xx/5xx)
- Add configurable latency
- Record and replay requests
- Export as Postman/Insomnia collections

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
