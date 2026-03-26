# Schema Drift Detector

Agent that detects drift between database migration files and ORM model definitions. Compares the expected schema (from sequential migrations) against ORM models (Prisma, Drizzle, TypeORM, SQLAlchemy) and flags mismatches — missing columns, type discrepancies, index gaps, and orphaned relations.

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

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
