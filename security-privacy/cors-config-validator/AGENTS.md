# AGENTS.md — CORS Config Validator

## Overview
Analyzes CORS configurations across APIs, flags overly permissive or broken setups. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse CORS headers from responses
- Detect wildcard origin allowances
- Flag missing credentials handling
- Test preflight request behavior
- Identify mismatched configurations
- Suggest restrictive CORS policies
- Generate configuration templates
- Support Express/Django/FastAPI configs

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
