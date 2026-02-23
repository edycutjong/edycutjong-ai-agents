# AGENTS.md — dependency-bloat-reducer

## Overview
Find heavy/unused dependencies.

## Tech Stack
- **Runtime:** Python 3.11+
- **AI:** LangChain / OpenAI / AST Parsing
- **Git:** GitPython / PyGithub

## Features
- Analyze bundle size\n- Cost per package\n- Find unused exports\n- Suggest lighter alternatives\n- Tree-shaking audit\n- Duplicate package check\n- Visualize graph\n- Remove generation

## File Structure
- `agent.py`: Logic
- `tools/`: Fixer tools
- `tests/`: Verification

## Design Notes
Treemap visualization.

## Commands
python3 agent.py
