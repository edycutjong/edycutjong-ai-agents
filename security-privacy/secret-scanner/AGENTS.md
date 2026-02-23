# AGENTS.md — Secret Scanner

## Overview
Deep-scans repositories for leaked API keys, passwords, tokens, and certificates. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan files for secret patterns (regex)
- Detect API keys across 50+ providers
- Find hardcoded passwords and tokens
- Check git history for leaked secrets
- Generate remediation report
- Suggest secret rotation steps
- Support custom secret patterns
- Pre-commit hook integration

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
