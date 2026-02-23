# AGENTS.md — Password Strength Analyzer

## Overview
Evaluates password policies and authentication implementations in codebases. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Analyze password validation logic
- Check against NIST/OWASP guidelines
- Detect weak hashing algorithms
- Flag missing rate limiting
- Review MFA implementation
- Suggest password policy improvements
- Check for credential stuffing protection
- Generate security assessment report

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
