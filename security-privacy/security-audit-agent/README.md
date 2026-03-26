# Security Audit Agent

AI agent that scans codebases for security vulnerabilities (XSS, SQL injection, etc.) and suggests fixes.

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
