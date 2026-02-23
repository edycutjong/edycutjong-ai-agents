# AGENTS.md — code-style-enforcer-bot

## Overview
Friendly bot to enforce and fix style.

## Tech Stack
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Comment on style vios\n- Auto-fix simple issues\n- Explain rule rationale\n- Detect 'vibe' violations\n- Learn from codebase\n- Gamification stats\n- Custom tone\n- Ignore config

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Design Notes
Chat bot interface.

## Commands
python3 agent.py
