# AGENTS.md — Regex Builder

## Overview
Takes natural language descriptions and generates, explains, and tests regex patterns. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Convert English to regex patterns
- Explain existing regex step-by-step
- Test regex against sample strings
- Show match groups and captures
- Generate regex for common patterns (email, URL, etc.)
- Support multiple regex flavors (JS, Python, Go)
- Visualize regex as railroad diagram
- Suggest optimized patterns

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
