# AGENTS.md — vuln-auto-patcher

## Overview
Auto-patch known security vulnerabilities.

## Tech Stack
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Ingest audit report (npm/cve)\n- Find minimal version bump\n- Check breaking changes\n- Run test suite\n- Bisect if failing\n- Create PR\n- Notify security team\n- Lockfile update

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Design Notes
Automated pipeline.

## Commands
python3 agent.py
