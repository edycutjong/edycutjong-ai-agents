# Api Key Rotator

Automated secret rotation agent that scans codebases for exposed API keys, tracks key expiration, and assists with secure rotation workflows.

## Features
- Codebase scanning for exposed secrets
- Key expiration tracking
- Rotation schedule management
- Secure key generation
- Environment file auditing
- Git history secret detection
- Rotation runbook generation
- Integration with secret managers (Vault, AWS SM)

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
