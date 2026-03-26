# Migration Checker

Agent that validates database migration files — checks for destructive operations, naming, and ordering.

## Features
- Parse SQL migration files
- Detect destructive operations (DROP, TRUNCATE)
- Naming convention validation
- Sequential ordering check
- Reversibility assessment
- Schema conflict detection
- PR comment with findings
- Configurable rules
- Support Prisma, Drizzle, raw SQL
- Exit codes for CI

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
