# Qa Test Generator

Agent that reads features/code and generates Cypress/Playwright tests.

## Features
- Parse UI components\n- Generate test scenarios\n- Write executable test code\n- Mock API responses\n- Self-healing tests (update selectors)\n- Integration with test runner\n- Coverage analysis\n- Edge case generation

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
