# Deprecation Hunter

Finds and intends to fix deprecated usage.

## Features
- Scan dependencies\n- Find deprecated calls\n- Suggest replacements\n- Generate refactor PR\n- Safety check tests\n- Group by library\n- Priority sorting\n- Report generation

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
