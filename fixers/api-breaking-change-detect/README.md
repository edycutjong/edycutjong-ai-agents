# Api Breaking Change Detect

Detect breaking API changes before merge.

## Features
- Compare OpenAPI specs\n- Detect removal/rename\n- Type changes\n- Client impact analysis\n- Version bump suggestion\n- Changelog generation\n- Block PR option\n- Notify consumers

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
