# Changelog Writer

Release note agent — Analyze git commit range.

## Features
- Analyze git commit range
- Group by feat/fix/chore
- Summarize changes
- Generate markdown output
- Publish to release

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
