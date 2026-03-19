# Api Schema Migrator Agent

## Overview
Detects breaking changes between OpenAPI spec versions and generates migration code for API consumers.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Compare two OpenAPI/Swagger specs
- Detect breaking vs non-breaking changes
- Generate migration code snippets
- Support REST and GraphQL schemas
- Create changelog from diff
- Type mapping for renamed fields
- Request/response body migration
- Header and auth changes detection
- Export migration guide as markdown
- Configurable ignore rules

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
