# AGENTS.md — Schema Drift Detector

## Overview
Agent that detects drift between database migration files and ORM model definitions. Compares the expected schema (from sequential migrations) against ORM models (Prisma, Drizzle, TypeORM, SQLAlchemy) and flags mismatches — missing columns, type discrepancies, index gaps, and orphaned relations.

## References
- Inspired by [Atlas](https://atlasgo.io/) — declarative schema-as-code with drift detection
- Inspired by [Prisma Migrate](https://www.prisma.io/docs/orm/prisma-migrate) — schema-first migration generation

## Tech Stack
- **Stack:** Python 3.11+
- **Build:** `pip install -r requirements.txt`
- **Dependencies:** sqlparse, pyyaml, click

## Features
- Parse SQL migration files (up/down) into cumulative schema state
- Parse ORM model definitions (Prisma `.prisma`, Drizzle `.ts`, SQLAlchemy `.py`)
- Column-level diff: name, type, nullable, default value
- Index and unique constraint comparison
- Foreign key and relation validation
- Detect orphaned migrations (applied but model removed)
- Detect shadow columns (in model but no migration)
- Generate human-readable drift report (Markdown table)
- JSON output for CI pipeline integration
- Exit code 1 on drift detected, 0 on clean

## File Structure
- `main.py` — CLI entry point (click-based)
- `lib/migration_parser.py` — SQL migration file parser
- `lib/orm_parser.py` — ORM model definition parser
- `lib/differ.py` — Schema comparison engine
- `lib/reporter.py` — Markdown and JSON report generator
- `requirements.txt` — Python dependencies
- `tests/` — Unit tests with fixture migrations
- `README.md` — Usage documentation

## Design Guidelines
- **Theme:** Dark minimal with amber accents
- **Primary:** `#F59E0B` (Amber)
- **Secondary:** `#FBBF24` (Light Amber)
- **Accent:** `#EF4444` (Red — for drift warnings)
- **Background:** `#0F172A` (Slate)
- **Font:** JetBrains Mono (terminal output)
- **Style:** Clean CLI output with color-coded diffs

## Requirements
- No external API keys required
- Supports PostgreSQL, MySQL, SQLite migration syntax
- CLI-friendly with `--format json|markdown|table` flag
- CI integration with non-zero exit codes on drift
- Extensible parser architecture for new ORM adapters
