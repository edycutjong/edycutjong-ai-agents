# AGENTS.md — Tech Debt Scorer

## Overview
Agent that scans a codebase and scores technical debt by category — complexity, duplication, outdated deps, test gaps.

## Tech Stack
- **Stack:** Python

## Features
- Scan source files for complexity metrics
- Cyclomatic complexity scoring
- Code duplication detection
- Outdated dependency counting
- Test coverage gap analysis
- TODO/FIXME/HACK comment counting
- Large file detection
- Deep nesting warnings
- Overall debt score 0-100
- JSON report with actionable items

## File Structure
- `main.py` — Entry point
- `lib/` — Core logic
- `requirements.txt`
- `README.md`

## Requirements
- No external API keys
- CLI-friendly with JSON output
- CI integration support
