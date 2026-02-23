# AGENTS.md — License Compliance Checker

## Overview
Audits project dependencies for license conflicts (GPL vs MIT vs proprietary). Designed as an AI agents project.

## Tech
- Python 3.10+
- AutoGen / CrewAI / LangChain
- OpenAI API / Gemini API

## Features
- Scan package.json/requirements.txt/Cargo.toml
- Identify license for each dependency
- Flag incompatible license combinations
- Generate license compliance report
- Detect copyleft contamination risk
- Support SPDX license identifiers
- Export SBOM (Software Bill of Materials)
- Suggest compliant alternatives

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
