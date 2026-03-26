# Gdpr Compliance Checker

Privacy compliance agent that scans codebases for PII handling patterns, consent mechanisms, and data retention policy violations.

## Features
- PII detection in code & data
- Consent flow analysis
- Data retention policy checker
- Right-to-deletion compliance
- Cookie consent verification
- Privacy policy generator
- DPIA (Data Protection Impact Assessment) template
- Compliance report with GDPR article references

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
