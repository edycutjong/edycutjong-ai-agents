# Pr Reviewer

Autonomous agent that reviews pull requests — checks code quality, suggests improvements, and flags issues.

## Features
- GitHub webhook integration
- Code diff analysis
- Style and convention checking
- Security vulnerability detection
- Performance anti-pattern warnings
- Inline comment suggestions
- Summary review comment generation
- Configurable rule sets
- Ignore patterns for generated files
- Review approval thresholds

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
