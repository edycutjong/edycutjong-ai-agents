# AGENTS.md — Incident Responder

## Overview
Monitors logs, detects anomalies, and auto-generates incident reports with root cause analysis. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Monitor application logs in real-time
- Detect anomalies and error spikes
- Correlate errors across services
- Generate root cause analysis
- Create incident reports (Markdown/PDF)
- Suggest remediation steps
- Track incident timeline
- Integrate with PagerDuty/Slack alerts

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
