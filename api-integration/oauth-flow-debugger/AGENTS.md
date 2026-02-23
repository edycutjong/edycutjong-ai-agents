# AGENTS.md — OAuth Flow Debugger

## Overview
Traces OAuth 2.0 flows step-by-step, identifies misconfigurations, and suggests fixes. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Trace authorization code flow
- Trace client credentials flow
- Inspect token payloads (JWT decode)
- Validate redirect URI configurations
- Check scope permissions
- Detect common misconfigurations
- Generate flow sequence diagrams
- Test token refresh cycles

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
