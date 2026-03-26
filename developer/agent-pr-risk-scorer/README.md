# Pr Risk Scorer

Analyzes pull requests for risk signals (large diffs, auth code changes, missing tests) and assigns a composite risk score.

## Features
- Parse PR diffs and file changes
- Detect auth/security code modifications
- Check for missing test coverage
- Calculate composite risk score (1-10)
- Flag large PRs exceeding threshold
- Detect database migration changes
- Check for hardcoded secrets
- Generate risk report summary
- Configurable risk weights
- PR comment with findings

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
