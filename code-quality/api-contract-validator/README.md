# Api Contract Validator

Agent that compares API implementation against OpenAPI spec and reports drift — missing fields, type mismatches.

## Features
- Parse OpenAPI/Swagger spec
- Parse API route implementation code
- Detect missing endpoints
- Detect extra undocumented endpoints
- Type mismatch detection
- Required field validation
- Response schema validation
- Deprecation warnings
- Generate drift report
- CI-friendly exit codes

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
