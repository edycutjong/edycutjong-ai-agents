# AGENTS.md — doc-drift-fixer

## Overview
Aligns documentation with code changes.

## Tech
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Connect to Git\n- Analyze PR diffs\n- Scan related docs\n- Propose doc updates\n- Verify code examples\n- Check outdated links\n- Comment on PR\n- Commit changes

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Commands
python3 agent.py
