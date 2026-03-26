# Sql Query Optimizer

Takes slow SQL queries, analyzes EXPLAIN plans, and suggests index additions and query rewrites for better performance.

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

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
