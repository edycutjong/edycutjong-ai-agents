# Autogen Agent

## Overview
A conversational AI system with multiple agents that can write code, debug, and execute tasks collaboratively. Built with Microsoft AutoGen.

## Tech
- Python 3.10+
- AutoGen
- OpenAI API

## Features
- AssistantAgent: plans and writes code
- UserProxyAgent: executes code and provides feedback
- GroupChat: multi-agent discussion for complex problems
- Code execution sandbox (Docker or local)
- Automated debugging: retry with error feedback
- Task types: code generation, data analysis, math problems
- Conversation logging and export
- Configurable agent personalities and system prompts

## File Structure
- `README.md` — Documentation
- `agents/` — Agents module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tasks/` — Tasks module
- `tests/` — Tests module

## API Keys
- `OPENAI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
