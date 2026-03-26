# Log Noise Reducer

Identify spammy logs to cleanup.

## Features
- Analyze production logs\n- Find high volume\n- Identify source line\n- Suggest level change (Info->Debug)\n- Remove print statements\n- Sampling suggestion\n- Cost impact\n- Jira creation

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
