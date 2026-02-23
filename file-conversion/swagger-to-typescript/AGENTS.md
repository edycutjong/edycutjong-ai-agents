# AGENTS.md — Swagger to TypeScript

## Overview
Generates TypeScript interfaces and API client code from OpenAPI/Swagger specifications. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse OpenAPI 3.0/Swagger 2.0 specs
- Generate TypeScript interfaces
- Create typed API client functions
- Handle nullable and optional fields
- Generate enum types
- Support request/response types
- Create axios/fetch wrappers
- Export as npm package structure

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
