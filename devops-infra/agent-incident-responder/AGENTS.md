# Incident Responder

## Overview
Monitors application logs and metrics, auto-diagnoses issues, and suggests or applies remediation steps.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Monitor log files in real-time
- Detect error patterns and anomalies
- Auto-diagnose common issues
- Suggest remediation steps
- Apply automated fixes when safe
- Generate incident reports
- Escalation rules configuration
- Post-mortem template generation

## File Structure
- `agent/` — Agent module
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
