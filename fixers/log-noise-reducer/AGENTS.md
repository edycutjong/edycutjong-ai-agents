# AGENTS.md — log-noise-reducer

## Overview
Identify spammy logs to cleanup.

## Tech
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Analyze production logs\n- Find high volume\n- Identify source line\n- Suggest level change (Info->Debug)\n- Remove print statements\n- Sampling suggestion\n- Cost impact\n- Jira creation

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Commands
python3 agent.py
