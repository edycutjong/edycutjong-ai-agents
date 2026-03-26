# Api Monitor

An AI agent that continuously monitors API endpoints for uptime, response time degradation, schema changes, and contract violations.

## Features
- Periodic endpoint health checks
- Response time tracking
- Schema drift detection
- Status code monitoring
- Alert threshold configuration
- Historical uptime reports
- Response body diff detection
- Certificate expiry warnings
- Rate limit tracking
- Incident timeline generation

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
