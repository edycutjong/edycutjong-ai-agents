# Dependency Advisor Agent

## Overview
Scans package.json/requirements.txt for CVEs, outdated packages, and suggests upgrade paths with migration guides.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse package.json and requirements.txt
- Check NPM/PyPI for latest versions
- Query CVE databases for vulnerabilities
- Generate upgrade priority list
- Create migration guides for breaking changes
- Detect unused dependencies
- License compatibility checking
- Suggest lighter alternatives
- Export dependency report
- Configurable severity thresholds

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
