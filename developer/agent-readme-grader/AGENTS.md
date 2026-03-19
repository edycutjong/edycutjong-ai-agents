# Readme Grader Agent

## Overview
Scores repository READMEs on completeness and quality, suggesting specific improvements.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Score README on 10-point scale
- Check for required sections (install, usage, API)
- Verify badge presence and validity
- Assess documentation depth
- Check for contributing guidelines
- Verify license information
- Evaluate code example quality
- Check for broken links
- Suggest missing sections
- Generate improvement checklist

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
