# AGENTS.md — CI Pipeline Optimizer

## Overview
Analyzes CI/CD configurations, identifies bottlenecks, and suggests parallelization and caching strategies. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse GitHub Actions/GitLab CI configs
- Identify slow pipeline stages
- Suggest parallelization strategies
- Recommend caching improvements
- Estimate time savings
- Generate optimized config files
- Compare before/after metrics
- Support multi-provider configs

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
