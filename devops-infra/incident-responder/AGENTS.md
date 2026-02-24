# Incident Responder

## Overview
Monitors logs, detects anomalies, and auto-generates incident reports with root cause analysis.

## Tech
- Python 3.10+
- CrewAI
- LangChain
- AutoGen
- Gemini API

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
- `README.md` — Documentation
- `agent/` — Agent module
- `app.py` — Application entry
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `prompts/` — Prompts module
- `reports/` — Reports module
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## API Keys
- `GEMINI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
