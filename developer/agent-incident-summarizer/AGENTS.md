# Incident Summarizer Agent

## Overview
Parses application logs and alerts to generate structured incident summaries with timeline and root cause analysis.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse structured and unstructured logs
- Build incident timeline
- Identify error patterns and clusters
- Generate root cause hypothesis
- Create severity classification
- Extract affected services/endpoints
- Suggest remediation steps
- Support multiple log formats (JSON, syslog)
- Generate postmortem template
- Configurable alert thresholds

## File Structure
- `agent/main.py — entry point`
- `agent/core.py — core logic`
- `agent/utils.py — helper functions`
- `tests/test_core.py — unit tests`
- `requirements.txt — dependencies`
- `README.md — documentation`

## Design Guidelines
- **Theme:** Dark mode with Arctic Blue palette
- **Primary:** `#3B82F6`
- **Accent:** `#F59E0B`
- **Background:** `#0A1022`
- **Border Radius:** 12px

## Requirements
- Fully functional — no placeholder content
- Configurable via environment variables
- Comprehensive error handling and logging
