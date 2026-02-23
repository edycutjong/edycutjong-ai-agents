# AGENTS.md — Log Analyzer

## Overview
Ingests application logs, identifies patterns, and surfaces errors with context. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse structured and unstructured logs
- Identify error patterns and frequencies
- Cluster similar log entries
- Timeline visualization of events
- Extract stack traces with context
- Generate summary reports
- Filter by severity/service/time
- Export findings as Markdown

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
