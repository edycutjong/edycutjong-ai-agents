# Tech Debt Scorer

Agent that scans a codebase and scores technical debt by category — complexity, duplication, outdated deps, test gaps.

## Features
- Scan source files for complexity metrics
- Cyclomatic complexity scoring
- Code duplication detection
- Outdated dependency counting
- Test coverage gap analysis
- TODO/FIXME/HACK comment counting
- Large file detection
- Deep nesting warnings
- Overall debt score 0-100
- JSON report with actionable items

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
