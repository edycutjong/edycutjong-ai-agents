# AGENTS.md — API Contract Validator

## Overview
Agent that compares API implementation against OpenAPI spec and reports drift — missing fields, type mismatches.

## Tech Stack
- **Stack:** Python

## Features
- Parse OpenAPI/Swagger spec
- Parse API route implementation code
- Detect missing endpoints
- Detect extra undocumented endpoints
- Type mismatch detection
- Required field validation
- Response schema validation
- Deprecation warnings
- Generate drift report
- CI-friendly exit codes

## File Structure
- `main.py` — Entry point
- `lib/` — Core logic
- `requirements.txt`
- `README.md`

## Requirements
- No external API keys
- CLI-friendly with JSON output
- CI integration support
