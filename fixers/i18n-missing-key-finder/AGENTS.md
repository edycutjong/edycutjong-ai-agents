# AGENTS.md — i18n-missing-key-finder

## Overview
Find missing translation keys.

## Tech
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Scan code for tags\n- Compare locale files\n- Identify missing keys\n- Auto-translate (Draft)\n- Find unused keys\n- Consistency check\n- Structure sync\n- Export report

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Commands
python3 agent.py
