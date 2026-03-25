# Dead Code Finder Agent

## Overview
Agent that statically analyzes a Python codebase to find unused imports, unreachable code, unused variables, and unused definitions.

## Tech Stack
- **Stack:** Python

## Features
- Find unused imported modules
- Detect unreachable code paths (after return/raise/break)
- Identify unused function and class definitions
- Recursive directory scanning with ignore patterns
- Generate removal report with line numbers
- Confidence scoring per finding
- Safe-to-delete recommendations

## Commands
- Run: `python main.py <directory>`
- Test: `python -m pytest tests/ -v`

## Design Guidelines
- **Theme:** Dark mode
- **Primary:** `#EC4899`
- **Accent:** `#DB2777`
- **Background:** `#0D1117`

## Requirements
- No external API keys required for core features
- Works standalone and self-contained
- Python 3.9+
