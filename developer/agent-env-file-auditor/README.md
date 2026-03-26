# Env File Auditor

Scans .env files for leaked secrets, missing variables, and inconsistencies across development environments.

## Features
- Scan .env files for secret patterns
- Compare .env vs .env.example
- Detect high-entropy strings (potential secrets)
- Cross-reference environment variables
- Check for common misconfigurations
- Validate required variables exist
- Detect duplicate keys
- Flag insecure default values
- Generate environment audit report
- Support multiple .env file formats

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
