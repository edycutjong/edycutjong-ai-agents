# AGENTS.md — API Rate Limit Tester

## Overview
Stress-tests APIs to map rate limits and generates usage documentation. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Send configurable request bursts
- Detect rate limit headers (X-RateLimit)
- Map rate limit thresholds
- Identify rate limit reset windows
- Generate rate limit documentation
- Test different auth levels
- Visualize rate limit curves
- Suggest client-side throttling

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
