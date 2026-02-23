# AGENTS.md — css-dead-code-remover

## Overview
Identify unused CSS selectors.

## Tech
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Crawl pages/components\n- Match selectors\n- Identify coverage\n- Purge capabilities\n- Safe-list checking\n- Media query audits\n- Visual regression check\n- Minify

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Commands
python3 agent.py
