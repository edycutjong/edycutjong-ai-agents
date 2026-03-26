# Database Migration Reviewer

Agent that reviews SQL migration files for safety — checks for data loss, reversibility, index impact, and lock duration.

## Features
- Parse SQL migration files
- Detect destructive operations (DROP, TRUNCATE)
- Check for reversibility (UP/DOWN)
- Index impact analysis
- Lock duration estimation
- Large table warnings
- Data type change safety check
- Foreign key impact analysis
- Generate safety report
- Block/warn/pass classification

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
