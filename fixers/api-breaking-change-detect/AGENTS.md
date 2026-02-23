# AGENTS.md — api-breaking-change-detect

## Overview
Detect breaking API changes before merge.

## Tech
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Compare OpenAPI specs\n- Detect removal/rename\n- Type changes\n- Client impact analysis\n- Version bump suggestion\n- Changelog generation\n- Block PR option\n- Notify consumers

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Commands
python3 agent.py
