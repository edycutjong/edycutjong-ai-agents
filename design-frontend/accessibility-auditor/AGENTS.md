# AGENTS.md — Accessibility Auditor

## Overview
Scans HTML pages for WCAG 2.1 violations and generates prioritized fix suggestions. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Run automated WCAG 2.1 checks
- Check color contrast ratios
- Validate ARIA label usage
- Test keyboard navigation flow
- Check image alt text coverage
- Validate form label associations
- Generate prioritized fix list
- Score overall accessibility level

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
