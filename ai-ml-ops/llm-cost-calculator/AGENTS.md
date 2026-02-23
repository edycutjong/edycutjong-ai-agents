# AGENTS.md — LLM Cost Calculator

## Overview
Tracks token usage across AI providers, forecasts costs, and suggests optimizations. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse API usage logs
- Calculate costs per provider/model
- Forecast monthly spending
- Identify high-cost queries
- Suggest model downgrades for savings
- Compare provider pricing
- Generate cost breakdown reports
- Set budget alerts and thresholds

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
