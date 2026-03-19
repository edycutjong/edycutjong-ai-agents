# Codebase Onboarder Agent

## Overview
Generates 'Getting Started' guides by analyzing repo structure, README, package files, and key source files.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Scan repository file structure
- Parse README and documentation
- Identify tech stack from config files
- Generate setup instructions
- Map key directories and their purposes
- Extract environment variable requirements
- Create architecture overview diagram
- List available scripts and commands
- Identify testing framework and patterns
- Export as markdown getting-started guide

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
