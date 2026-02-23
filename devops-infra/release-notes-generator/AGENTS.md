# AGENTS.md — Release Notes Generator

## Overview
Reads git history between tags and generates polished, categorized release notes. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse git log between tags/commits
- Categorize changes (feat/fix/chore/breaking)
- Generate Markdown release notes
- Include contributor attribution
- Link to PR/issue references
- Auto-detect semantic versioning
- Support conventional commits
- Export to GitHub Releases format

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
