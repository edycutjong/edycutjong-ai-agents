# AI Hallucination Detector

Cross-references AI outputs against source documents and flags fabricated claims.

## Features
- Accept AI output and source documents
- Extract factual claims from output
- Verify claims against sources
- Score confidence per claim
- Flag unsupported statements
- Generate fact-check report
- Support multiple document formats
- Highlight fabricated references

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
