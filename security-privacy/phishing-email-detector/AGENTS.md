# AGENTS.md — Phishing Email Detector

## Overview
Analyzes email headers and content to flag phishing attempts with confidence scores. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse email headers (SPF/DKIM/DMARC)
- Analyze sender reputation
- Detect suspicious URLs and domains
- Identify social engineering patterns
- Score phishing probability
- Extract and check embedded links
- Generate safety report
- Support EML/MSG file formats

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
