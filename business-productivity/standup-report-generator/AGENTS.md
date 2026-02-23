# AGENTS.md — Standup Report Generator

## Overview
Reads git commits and issue trackers, auto-generates daily standup reports. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse recent git commits
- Read Jira/Linear/GitHub issues
- Generate 'Yesterday/Today/Blockers' format
- Summarize code changes in plain English
- Link to relevant PRs and issues
- Support team-wide rollup reports
- Schedule daily generation
- Post to Slack/Teams via webhook

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
