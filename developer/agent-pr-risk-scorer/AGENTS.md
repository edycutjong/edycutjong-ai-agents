# Pr Risk Scorer Agent

## Overview
Analyzes pull requests for risk signals (large diffs, auth code changes, missing tests) and assigns a composite risk score.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse PR diffs and file changes
- Detect auth/security code modifications
- Check for missing test coverage
- Calculate composite risk score (1-10)
- Flag large PRs exceeding threshold
- Detect database migration changes
- Check for hardcoded secrets
- Generate risk report summary
- Configurable risk weights
- PR comment with findings

## File Structure
- `agent/main.py — entry point`
- `agent/core.py — core logic`
- `agent/utils.py — helper functions`
- `tests/test_core.py — unit tests`
- `requirements.txt — dependencies`
- `README.md — documentation`

## Design Guidelines
- **Theme:** Dark mode with Arctic Blue palette
- **Primary:** `#3B82F6`
- **Accent:** `#F59E0B`
- **Background:** `#0A1022`
- **Border Radius:** 12px

## Requirements
- Fully functional — no placeholder content
- Configurable via environment variables
- Comprehensive error handling and logging
