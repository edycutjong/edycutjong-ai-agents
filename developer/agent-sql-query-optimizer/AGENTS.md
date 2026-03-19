# Sql Query Optimizer Agent

## Overview
Takes slow SQL queries, analyzes EXPLAIN plans, and suggests index additions and query rewrites for better performance.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** LangChain / OpenAI SDK
- **Build:** `pip install -r requirements.txt`

## Features
- Parse SQL queries for analysis
- Generate EXPLAIN plan interpretation
- Suggest missing indexes
- Identify N+1 query patterns
- Rewrite subqueries as JOINs
- Detect full table scans
- Suggest query caching strategies
- Support PostgreSQL and MySQL dialects
- Benchmark before/after estimates
- Generate optimization report

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
