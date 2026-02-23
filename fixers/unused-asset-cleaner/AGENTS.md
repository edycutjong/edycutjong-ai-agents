# AGENTS.md — unused-asset-cleaner

## Overview
Find and remove unused images/files.

## Tech Stack
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Scan source code\n- Scan asset folders\n- Graph dependencies\n- Identify orphans\n- Move to trash/backup\n- Confirm before delete\n- Optimize remaining\n- Report savings

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Design Notes
File list UI.

## Commands
python3 agent.py
