# AGENTS.md — Prompt Optimizer

## Overview
Takes AI prompts, runs A/B variants, measures output quality, and suggests improvements. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept input prompts and test cases
- Generate prompt variations
- Run A/B tests against LLM APIs
- Score outputs for quality/relevance
- Suggest optimized prompts
- Track prompt version history
- Compare across different models
- Export results as report

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
