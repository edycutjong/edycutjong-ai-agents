# AGENTS.md — Privacy Policy Generator

## Overview
Reads application code, identifies data collection patterns, and generates GDPR/CCPA-compliant privacy policies. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan code for data collection points
- Identify PII handling (email, location, etc.)
- Generate GDPR-compliant privacy policy
- Generate CCPA-compliant privacy policy
- Support multiple output formats (MD/HTML)
- Track third-party data sharing
- Include cookie policy sections
- Version and date policies automatically

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
