# Vuln Auto Patcher

Auto-patch known security vulnerabilities.

## Features
- Ingest audit report (npm/cve)\n- Find minimal version bump\n- Check breaking changes\n- Run test suite\n- Bisect if failing\n- Create PR\n- Notify security team\n- Lockfile update

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
