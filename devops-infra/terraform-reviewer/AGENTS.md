# AGENTS.md — Terraform Reviewer

## Overview
Reviews Terraform and IaC plans, flags security risks and cost implications. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse Terraform HCL files
- Flag security misconfigurations
- Estimate resource costs
- Detect drift from state
- Suggest best practices
- Validate naming conventions
- Check for hardcoded values
- Generate review report

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
