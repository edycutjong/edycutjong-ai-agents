# Changelog Drafter Agent

## Overview
Reads git log between tags and drafts human-readable changelogs with automatic categorization.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse git log between version tags
- Categorize commits (feat/fix/docs/chore)
- Group by component or scope
- Generate markdown changelog
- Support conventional commits
- Detect breaking changes
- Link to PR/issue numbers
- Configurable category mappings
- Support monorepo structures
- Export for GitHub Releases

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
