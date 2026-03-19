# Git Conflict Resolver Agent

## Overview
Parses git merge conflicts and suggests semantic resolutions based on understanding both sides of changes.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse conflict markers in files
- Analyze both sides of conflicts
- Suggest resolution based on semantic analysis
- Handle common patterns (imports, configs)
- Preserve formatting consistency
- Detect overlapping changes
- Support multiple file types
- Generate resolution preview
- Confidence scoring per resolution
- Batch resolve similar conflicts

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
