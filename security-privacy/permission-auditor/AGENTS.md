# AGENTS.md — Permission Auditor

## Overview
Scans app manifests and configurations for excessive permissions and suggests removals. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Android/iOS manifests
- Analyze Chrome extension permissions
- Compare declared vs used permissions
- Flag unnecessary permissions
- Suggest minimal permission set
- Generate permission justification docs
- Check OAuth scope minimality
- Support web app permission policies

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
