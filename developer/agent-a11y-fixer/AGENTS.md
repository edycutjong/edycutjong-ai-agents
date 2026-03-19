# A11Y Fixer Agent

## Overview
Scans HTML for accessibility issues and auto-generates fixes including alt text, ARIA labels, and contrast improvements.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Scan HTML for WCAG violations
- Auto-generate alt text for images
- Add missing ARIA labels and roles
- Fix heading hierarchy issues
- Detect color contrast failures
- Generate skip navigation links
- Fix form label associations
- Add keyboard navigation support
- Generate accessibility audit report
- Apply fixes as HTML patches

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
