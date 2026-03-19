# Test Case Generator Agent

## Overview
Analyzes function signatures and generates comprehensive unit test cases including edge cases and error scenarios.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse function signatures and types
- Generate happy-path test cases
- Create edge case scenarios
- Generate error handling tests
- Support Python and TypeScript
- Mock external dependencies
- Generate test fixtures
- Boundary value analysis
- Coverage gap detection
- Export as pytest/jest files

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
