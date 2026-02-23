# AGENTS.md — AI Hallucination Detector

## Overview
Cross-references AI outputs against source documents and flags fabricated claims. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Accept AI output and source documents
- Extract factual claims from output
- Verify claims against sources
- Score confidence per claim
- Flag unsupported statements
- Generate fact-check report
- Support multiple document formats
- Highlight fabricated references

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
