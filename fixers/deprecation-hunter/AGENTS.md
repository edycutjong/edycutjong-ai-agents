# AGENTS.md — deprecation-hunter

## Overview
Finds and intends to fix deprecated usage.

## Tech Stack
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Scan dependencies\n- Find deprecated calls\n- Suggest replacements\n- Generate refactor PR\n- Safety check tests\n- Group by library\n- Priority sorting\n- Report generation

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Design Notes
Dashboard status.

## Commands
python3 agent.py
