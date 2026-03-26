# Migration Planner

Analyzes database schemas and generates migration plans with rollback strategies.

## Features
- Compare source and target schemas
- Generate step-by-step migration plan
- Create rollback procedures
- Estimate migration duration
- Identify breaking changes
- Generate migration SQL scripts
- Validate data integrity checks
- Support PostgreSQL/MySQL/SQLite

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
