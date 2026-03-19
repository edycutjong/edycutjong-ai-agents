# Docker Slimmer Agent

## Overview
Analyzes Dockerfiles and suggests optimizations for smaller images including multi-stage builds and layer caching.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse Dockerfile instructions
- Suggest multi-stage build patterns
- Recommend smaller base images
- Optimize layer ordering for caching
- Detect unnecessary packages
- Remove build-time only dependencies
- Estimate image size savings
- Suggest .dockerignore improvements
- Security scan base images
- Generate optimized Dockerfile

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
