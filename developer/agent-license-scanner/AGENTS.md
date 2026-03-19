# License Scanner Agent

## Overview
Scans all project dependencies for license types and flags incompatibilities with the project's license.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Scan npm/pip/cargo dependencies recursively
- Identify license type per package
- Check license compatibility matrix
- Flag copyleft in permissive projects
- Detect missing license files
- Generate SBOM (Software Bill of Materials)
- Support SPDX identifiers
- Create compliance report
- Configurable allowlist/blocklist
- Export for legal review

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
