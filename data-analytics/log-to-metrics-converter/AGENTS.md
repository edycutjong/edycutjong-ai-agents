# AGENTS.md — Log to Metrics Converter

## Overview
Parses unstructured application logs into structured metrics and dashboard configurations. Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Parse unstructured log formats
- Extract metrics (latency, error rates, throughput)
- Generate Prometheus metric definitions
- Create Grafana dashboard JSON
- Identify log format patterns
- Map log levels to alert thresholds
- Support multiple log formats
- Generate metric documentation

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
