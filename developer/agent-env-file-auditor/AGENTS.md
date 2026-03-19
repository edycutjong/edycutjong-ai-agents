# Env File Auditor Agent

## Overview
Scans .env files for leaked secrets, missing variables, and inconsistencies across development environments.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Scan .env files for secret patterns
- Compare .env vs .env.example
- Detect high-entropy strings (potential secrets)
- Cross-reference environment variables
- Check for common misconfigurations
- Validate required variables exist
- Detect duplicate keys
- Flag insecure default values
- Generate environment audit report
- Support multiple .env file formats

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
