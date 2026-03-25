# License Auditor Agent

## Overview
Agent that audits all Python project dependencies for license compliance, flags incompatible licenses, and generates a license report.

## Tech Stack
- **Stack:** Python

## Features
- Scan all installed Python packages
- Identify license type per package via importlib.metadata
- Flag copyleft licenses (GPL, AGPL)
- Detect missing license metadata
- Check license compatibility
- Generate THIRD_PARTY_LICENSES file
- Allowlist/blocklist configuration
- Report in Markdown/JSON/CSV
- CI pipeline integration (--fail-on-blocked)

## Commands
- Run: `python main.py --dir <project_dir>`
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
